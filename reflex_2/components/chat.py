import html


def js_escape(text: str) -> str:
    """JavaScriptのテンプレートリテラル用に安全にエスケープ"""
    return (
        text.replace("\\", r"\\")
        .replace("`", r"\u0060")
        .replace("$", r"\u0024")
        .replace("\n", r"\\n")
        .replace("'", r"\\'")
    )


import reflex as rx

from reflex_2.state import QA, State
from reflex.constants.colors import ColorType


def message_content(text: str, color: ColorType) -> rx.Component:
    """Create a message content component.

    Args:
        text: The text to display.
        color: The color of the message.

    Returns:
        A component displaying the message.
    """
    return rx.markdown(
        text,
        background_color=rx.color(color, 4),
        color=rx.color(color, 12),
        display="inline-block",
        padding_inline="1em",
        border_radius="8px",
    )


def message(qa: QA) -> rx.Component:
    """A single question/answer message."""
    # 質問バブル（そのまま）
    question_box = rx.box(
        message_content(qa["question"], "mauve"),
        text_align="right",
        margin_bottom="8px",
    )

    # 回答 + コピーアイコンを横並びにする
    answer_row = rx.hstack(
        # 回答バブル
        message_content(qa["answer"], "accent"),
        # コピーアイコンボタン
        rx.icon_button(
            rx.icon("copy", size=16),
            aria_label="Copy markdown",
            size="2",
            variant="soft",
            on_click=[
                rx.set_clipboard(qa["answer"]),
                rx.toast(title="Copied!", duration=1500),
            ],
            # 少し余白
            margin_left="4px",
        ),
        align_items="start",
    )

    return rx.box(
        question_box,
        answer_row,
        max_width="50em",
        margin_inline="auto",
        margin_bottom="16px",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.auto_scroll(
        rx.foreach(State.selected_chat, message),
        flex="1",
        padding="8px",
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.center(
        rx.vstack(
            rx.form(
                rx.hstack(
                    rx.input(
                        rx.input.slot(
                            rx.tooltip(
                                rx.icon("info", size=18),
                                content="Enter a question to get a response.",
                            )
                        ),
                        placeholder="Type something...",
                        id="question",
                        flex="1",
                    ),
                    rx.button(
                        "Send",
                        loading=State.processing,
                        disabled=State.processing,
                        type="submit",
                    ),
                    max_width="50em",
                    margin="0 auto",
                    align_items="center",
                ),
                reset_on_submit=True,
                on_submit=State.process_question,
            ),
            rx.text(
                "ReflexGPT may return factually incorrect or misleading responses. Use discretion.",
                text_align="center",
                font_size=".75em",
                color=rx.color("mauve", 10),
            ),
            rx.logo(margin_block="-1em"),
            width="100%",
            padding_x="16px",
            align="stretch",
        ),
        position="sticky",
        bottom="0",
        left="0",
        padding_y="16px",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        align="stretch",
        width="100%",
    )
