"""Build an offline skill ZIP from the pinned upstream guides."""

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def render_manifest(manifest, files):
    upstream = {key: value for key, value in manifest["upstream"].items() if key != "standaloneSha256"}
    contents = {
        **manifest,
        "upstream": upstream,
        "files": [
            {"path": name, "sha256": hashlib.sha256(content).hexdigest()}
            for name, content in sorted(files.items())
        ],
    }
    return (json.dumps(contents, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_upstream(lock, local_archive):
    archive_root = "skills-" + lock["revision"]
    if local_archive is None:
        url = f'https://codeload.github.com/{lock["repository"]}/tar.gz/{lock["revision"]}'
        with urlopen(url, timeout=40) as response:
            archive = response.read()
    else:
        archive = local_archive.read_bytes()

    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as source:
        for name, expected in lock["sha256"].items():
            member = source.getmember(f"{archive_root}/{name}")
            if not member.isfile():
                raise ValueError(f"Expected a regular upstream file: {name}")
            with source.extractfile(member) as file:
                content = file.read()
            if hashlib.sha256(content).hexdigest() != expected:
                raise ValueError(f"Upstream checksum mismatch: {name}")
            yield PurePosixPath(name), content


def render_entry(source, guide_paths, manifest):
    before_table, table_and_after = source.split("| 阶段 | 指引及依赖 | 完成依据 |\n", 1)
    table, after_table = table_and_after.split("\n\n", 1)
    table = re.sub(r"`([a-z0-9-]+)`", lambda match: f"@{guide_paths[match[1]]}", table)

    metadata = {
        "display_name": manifest["name"],
        "display_name_en": manifest["name_en"],
        "description_zh": manifest["description"],
        "description_en": "One entry point for Matt Pocock's The Main Flow, from requirements to review and retrospective. Includes the upstream guides. Independently maintained by vincent4j.",
        "examples_zh": manifest["examplePrompts"],
        "examples_en": [
            "Scope a feature and confirm its acceptance criteria with me.",
            "Resume this project task and show me the current stage.",
        ],
        "version": manifest["version"],
        "author": "vincent4j",
    }
    frontmatter = "".join(
        f"{name}: {json.dumps(value, ensure_ascii=False)}\n"
        for name, value in metadata.items()
    )
    entry = (
        before_table.replace("\n---\n", "\n" + frontmatter + "---\n", 1)
        + "| 阶段 | 指引及依赖 | 完成依据 |\n"
        + table
        + "\n\n"
        + after_table
    )
    return re.sub(
        r"\[([^\]]+)\]\((references/[^)#]+\.md)(?:#([^)]+))?\)",
        lambda match: f" @{match[2]} " + (f"的「{match[3]}」" if match[3] else ""),
        entry,
    ).encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-archive", type=Path, help="Reuse a downloaded upstream tar.gz")
    parser.add_argument("--global-suite", action="store_true", help="Build the WorkBuddy user-level installer bundle")
    args = parser.parse_args()
    try:
        output = build(PROJECT_ROOT, args.upstream_archive, args.global_suite)
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        parser.exit(1, f"离线打包失败：{error}\n")
    print(output)


def build(root, upstream_archive, global_suite=False):
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    if not isinstance(version, str) or not re.fullmatch(r"[0-9][0-9A-Za-z.+-]*", version):
        raise ValueError("manifest.json 的 version 必须是可用于文件名的版本号")

    source_files = {}
    for member in manifest["files"]:
        name = member["path"]
        content = (root / name).read_bytes()
        if hashlib.sha256(content).hexdigest() != member["sha256"]:
            raise ValueError(f"Source checksum mismatch: {name}")
        source_files[name] = content

    lock = manifest["upstream"]
    files = {
        name: source_files[name]
        for name in ("references/state.md", "references/setup.md", "references/implementation.md")
    }
    upstream_url = f'https://github.com/{lock["repository"]}/tree/{lock["revision"]}'
    files["references/mattpocock/NOTICE.md"] = (
        "# Upstream guides\n\n"
        f"Workflow guides by Matt Pocock, revision [{lock['revision']}]({upstream_url}). "
        "The guide documents are reproduced under the [MIT license](../mattpocock-LICENSE.txt). "
        "Matt Pocock Mainflow is independently maintained by vincent4j.\n"
    ).encode("utf-8")
    guide_paths = {}
    suite_skills = {}
    locked_files = lock["sha256"]
    if global_suite:
        lock = {**lock, "sha256": {**locked_files, **lock["standaloneSha256"]}}
    for source_path, content in read_upstream(lock, upstream_archive):
        if source_path.name == "LICENSE":
            files["references/mattpocock-LICENSE.txt"] = content
            continue
        guide = source_path.parts[2]
        is_entry = source_path.name == "SKILL.md"
        if global_suite:
            relative = PurePosixPath(*source_path.parts[2:])
            suite_skills[f"skills/{relative}"] = content
        if str(source_path) not in locked_files:
            continue
        filename = "guide.md" if is_entry else source_path.name
        destination = f"references/mattpocock/{guide}/{filename}"
        files[destination] = content
        if is_entry:
            guide_paths[guide] = destination

    files["SKILL.md"] = render_entry(source_files["SKILL.md"].decode("utf-8"), guide_paths, manifest)
    entry = files["SKILL.md"].decode("utf-8")
    for path in re.findall(r"@(references/[^\s|、，。]+\.md)", entry):
        if path not in files:
            raise ValueError(f"Missing runtime reference: {path}")

    files["manifest.json"] = render_manifest(manifest, files)
    if global_suite:
        suite_skills.update({f"skills/matt-mainflow/{name}": content for name, content in files.items()})
        for guide in guide_paths:
            suite_skills[f"skills/{guide}/LICENSE"] = files["references/mattpocock-LICENSE.txt"]
        suite_skills["install.py"] = (root / "packaging/install.py").read_bytes()
        suite_skills["README.md"] = (root / "packaging/README.md").read_bytes()
        bundle_files = suite_skills
        bundle_name = f"matt-mainflow-global-{version}"
    else:
        bundle_files = files
        bundle_name = "matt-mainflow"
    suffix = "global" if global_suite else "offline"
    output = root / "dist" / f"matt-mainflow-{suffix}-{version}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, delete=False) as temporary:
        staging_path = Path(temporary.name)
    try:
        with ZipFile(staging_path, "w") as bundle:
            for name, content in sorted(bundle_files.items()):
                member = ZipInfo(f"{bundle_name}/{name}")
                member.external_attr = 0o100644 << 16
                bundle.writestr(member, content, compress_type=ZIP_DEFLATED, compresslevel=9)
        staging_path.replace(output)
    finally:
        staging_path.unlink(missing_ok=True)
    return output


if __name__ == "__main__":
    main()
