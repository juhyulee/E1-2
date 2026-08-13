"""Quiz game entry point."""

from quiz_game.game import QuizGame


def main() -> None:
    """Start the application."""
    QuizGame().run()


if __name__ == "__main__":
    main()
