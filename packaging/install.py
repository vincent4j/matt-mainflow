"""Install the unpacked offline suite into WorkBuddy's user Skills folder."""

import argparse
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory


def install(source, destination):
    skills = sorted(source.iterdir())
    if not skills or not all((skill / "SKILL.md").is_file() for skill in skills):
        raise ValueError("安装包缺少独立 Skill 入口，请重新解压 ZIP。")

    destination.mkdir(parents=True, exist_ok=True)
    pending = []
    for skill in skills:
        target = destination / skill.name
        if not target.exists() and not target.is_symlink():
            pending.append(skill)
            continue
        if not all(
            (target / file.relative_to(skill)).is_file()
            and (target / file.relative_to(skill)).read_bytes() == file.read_bytes()
            for file in skill.rglob("*") if file.is_file()
        ):
            raise ValueError(f"已有同名 Skill 且内容不同，请先备份并移出安装目录：{target}")

    installed = []
    with TemporaryDirectory(prefix=".matt-mainflow-", dir=destination.parent) as temp:
        stage = Path(temp)
        for skill in pending:
            shutil.copytree(skill, stage / skill.name)
        try:
            for skill in pending:
                target = destination / skill.name
                if target.exists() or target.is_symlink():
                    raise FileExistsError(target)
                (stage / skill.name).rename(target)
                installed.append(target)
        except OSError:
            for target in reversed(installed):
                target.rename(stage / target.name)
            raise
    return [skill.name for skill in skills]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".workbuddy" / "skills")
    args = parser.parse_args()
    try:
        names = install(Path(__file__).resolve().parent / "skills", args.skills_dir.expanduser())
    except (OSError, ValueError) as error:
        parser.exit(1, f"安装失败：{error}\n")
    print(f"已就绪（{len(names)} 个用户级 Skill）：{', '.join(names)}")


if __name__ == "__main__":
    main()
