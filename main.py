from enum import Enum, auto

from questionary import select, Choice, Style


class WorkMod(Enum):
    CHOOSE = auto()
    CONSOLE = auto()
    APP = auto()
    EXIT = auto()


def main(work_mode: WorkMod) -> None:
    match work_mode:
        case WorkMod.CHOOSE:
            chosen: WorkMod = select(
                message="",
                choices=[
                    Choice("Запустить консольную версию", WorkMod.CONSOLE),
                    Choice("Запустить приложение", WorkMod.APP),
                    Choice("Выйти", WorkMod.EXIT),
                ],
                use_shortcuts=True,
                style=Style([
                    ('highlighted', 'bg:#1e4011 bold'),
                ]),
            ).ask()

            main(chosen)
        case WorkMod.CONSOLE:
            from console.src.main import Main

            Main().main()
        case WorkMod.APP:
            from app.src.main import Main

            Main().main()
        case WorkMod.EXIT:
            exit()


if __name__ == "__main__":
    CURRENT_WORK_MOD = WorkMod.CHOOSE

    main(CURRENT_WORK_MOD)
