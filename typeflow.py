import random
import time
import tkinter as tk
import customtkinter as ctk


SENTENCES = [
    "The quick brown fox jumps over the lazy dog",
    "Typing fast is a useful skill for coding",
    "Practice makes a person perfect in everything",
    "C programming is powerful and flexible",
    "Speed and accuracy matter in a typing test",
]

# Theme and color palette
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#10131A"
PANEL = "#191E29"
PANEL_LIGHT = "#202737"
TEXT = "#F3F5FA"
MUTED = "#929CAF"
ACCENT = "#7C83FF"
ACCENT_HOVER = "#696FF0"
GREEN = "#58D6A5"
RED = "#FF737D"
BORDER = "#2B3344"


class TypeFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TYPEFLOW — Typing Speed Test")
        self.geometry("980x760")
        self.minsize(760, 680)
        self.configure(fg_color=BG)

        self.current_sentence = ""
        self.started_at = None
        self.elapsed = 0.0
        self.timer_job = None
        self.test_active = False
        self.test_finished = False
        self.has_started_typing = False
        self.last_accuracy = 0.0
        self.last_wpm = 0.0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_stats()
        self._build_work_area()
        self._build_footer()

        self._set_sentence(random.choice(SENTENCES))
        self._set_status("Ready when you are. Press Start Test to begin.")
        self._refresh_stats()
        self._set_typing_enabled(False)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 18))
        header.grid_columnconfigure(0, weight=1)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.grid(row=0, column=0, sticky="ew")
        title_row.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            title_row,
            text="TYPEFLOW",
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
            text_color=TEXT,
        )
        title.grid(row=0, column=0, sticky="w")

        self.theme_button = ctk.CTkButton(
            title_row,
            text="☼  Toggle theme",
            width=132,
            height=34,
            corner_radius=10,
            fg_color=PANEL_LIGHT,
            hover_color=BORDER,
            text_color=TEXT,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._toggle_theme,
        )
        self.theme_button.grid(row=0, column=1, sticky="e")

        subtitle = ctk.CTkLabel(
            header,
            text="Test your speed. Improve your accuracy.",
            font=ctk.CTkFont(size=14),
            text_color=MUTED,
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))

        accent = ctk.CTkFrame(header, height=3, fg_color=ACCENT, corner_radius=3)
        accent.grid(row=2, column=0, sticky="ew", pady=(18, 0))

    def _build_stats(self):
        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.grid(row=1, column=0, sticky="ew", padx=32, pady=(0, 18))
        for col in range(3):
            stats.grid_columnconfigure(col, weight=1, uniform="stat")

        self.time_value = self._make_stat_card(stats, 0, "TIME ELAPSED", "00:00", "Timer starts on your first keystroke")
        self.wpm_value = self._make_stat_card(stats, 1, "TYPING SPEED", "0.0", "Words per minute")
        self.accuracy_value = self._make_stat_card(stats, 2, "ACCURACY", "100%", "Character match rate")

    def _make_stat_card(self, parent, col, label, value, hint):
        card = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=16,
            border_width=1,
            border_color=BORDER,
        )
        card.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 6, 0 if col == 2 else 6))
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=MUTED,
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 2))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=ACCENT if col == 1 else TEXT,
        )
        value_label.grid(row=1, column=0, sticky="w", padx=18)

        ctk.CTkLabel(
            card,
            text=hint,
            font=ctk.CTkFont(size=10),
            text_color=MUTED,
        ).grid(row=2, column=0, sticky="w", padx=18, pady=(0, 16))
        return value_label

    def _build_work_area(self):
        work = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=18, border_width=1, border_color=BORDER)
        work.grid(row=2, column=0, sticky="nsew", padx=32, pady=(0, 18))
        work.grid_columnconfigure(0, weight=1)
        work.grid_rowconfigure(2, weight=1)

        top = ctk.CTkFrame(work, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 8))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text="YOUR SENTENCE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=MUTED,
        ).grid(row=0, column=0, sticky="w")

        self.sentence_number = ctk.CTkLabel(
            top,
            text="RANDOM PRACTICE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=ACCENT,
        )
        self.sentence_number.grid(row=0, column=1, sticky="e")

        self.sentence_box = ctk.CTkTextbox(
            work,
            height=105,
            wrap="word",
            fg_color=PANEL_LIGHT,
            text_color=TEXT,
            border_width=1,
            border_color=BORDER,
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=19),
            activate_scrollbars=False,
        )
        self.sentence_box.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 18))
        self.sentence_box.configure(state="disabled")

        typing_header = ctk.CTkFrame(work, fg_color="transparent")
        typing_header.grid(row=2, column=0, sticky="new", padx=24, pady=(0, 8))
        typing_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            typing_header,
            text="YOUR TYPING",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=MUTED,
        ).grid(row=0, column=0, sticky="w")

        self.char_count_label = ctk.CTkLabel(
            typing_header,
            text="0 characters",
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
        )
        self.char_count_label.grid(row=0, column=1, sticky="e")

        self.typing_box = ctk.CTkTextbox(
            work,
            height=145,
            wrap="word",
            fg_color="#121722",
            text_color=TEXT,
            border_width=1,
            border_color=BORDER,
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=17),
            undo=True,
        )
        self.typing_box.grid(row=3, column=0, sticky="nsew", padx=24, pady=(0, 12))
        self.typing_box.bind("<KeyRelease>", self._on_key_release)
        self.typing_box.bind("<KeyPress>", self._on_key_press)
        self.typing_box.bind("<<Paste>>", self._on_paste)

        self.feedback_label = ctk.CTkLabel(
            work,
            text="Correct characters appear green; mistakes appear red.",
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
            anchor="w",
        )
        self.feedback_label.grid(row=4, column=0, sticky="ew", padx=24, pady=(0, 20))

        self.typing_box.tag_config("correct", foreground=GREEN)
        self.typing_box.tag_config("incorrect", foreground=RED)
        self.typing_box.tag_config("normal", foreground=TEXT)

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=32, pady=(0, 28))
        footer.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            footer,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=MUTED,
            anchor="w",
        )
        self.status_label.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        buttons = ctk.CTkFrame(footer, fg_color="transparent")
        buttons.grid(row=1, column=0, sticky="ew")
        buttons.grid_columnconfigure(4, weight=1)

        self.start_button = ctk.CTkButton(
            buttons,
            text="▶  Start Test",
            height=42,
            width=145,
            corner_radius=12,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.start_test,
        )
        self.start_button.grid(row=0, column=0, padx=(0, 10))

        self.finish_button = ctk.CTkButton(
            buttons,
            text="Finish Test",
            height=42,
            width=125,
            corner_radius=12,
            fg_color=PANEL_LIGHT,
            hover_color=BORDER,
            text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.finish_test,
            state="disabled",
        )
        self.finish_button.grid(row=0, column=1, padx=(0, 10))

        self.retry_button = ctk.CTkButton(
            buttons,
            text="↻  Try Again",
            height=42,
            width=125,
            corner_radius=12,
            fg_color=PANEL_LIGHT,
            hover_color=BORDER,
            text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.start_test,
        )
        self.retry_button.grid(row=0, column=2, padx=(0, 10))

        self.exit_button = ctk.CTkButton(
            buttons,
            text="Exit",
            height=42,
            width=85,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#3B2630",
            border_width=1,
            border_color="#65404A",
            text_color=RED,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.destroy,
        )
        self.exit_button.grid(row=0, column=3)

    def _set_sentence(self, sentence):
        self.current_sentence = sentence
        self.sentence_box.configure(state="normal")
        self.sentence_box.delete("1.0", "end")
        self.sentence_box.insert("1.0", sentence)
        self.sentence_box.configure(state="disabled")
        self.sentence_number.configure(text=f"{len(sentence)} CHARACTERS")

    def _set_status(self, message, color=MUTED):
        self.status_label.configure(text=message, text_color=color)

    def _set_typing_enabled(self, enabled):
        self.typing_box.configure(state="normal" if enabled else "disabled")

    def _toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current.lower() == "dark" else "dark")
        # The palette is deliberately designed for dark mode; the toggle uses
        # CustomTkinter's built-in appearance mode setting.

    def start_test(self):
        self._cancel_timer()
        self.current_sentence = random.choice(SENTENCES)
        self._set_sentence(self.current_sentence)

        self.typing_box.configure(state="normal")
        self.typing_box.delete("1.0", "end")
        self.typing_box.tag_remove("correct", "1.0", "end")
        self.typing_box.tag_remove("incorrect", "1.0", "end")
        self.typing_box.tag_remove("normal", "1.0", "end")

        self.started_at = None
        self.elapsed = 0.0
        self.test_active = True
        self.test_finished = False
        self.has_started_typing = False
        self.last_accuracy = 0.0
        self.last_wpm = 0.0

        self.start_button.configure(state="disabled")
        self.finish_button.configure(state="normal")
        self.retry_button.configure(state="normal")
        self._refresh_stats()
        self.char_count_label.configure(text="0 characters")
        self.feedback_label.configure(text="Start typing the sentence above. The timer begins with your first character.", text_color=MUTED)
        self._set_status("Test ready — your first keystroke starts the timer.", GREEN)
        self.typing_box.focus_set()

    def _on_key_press(self, event):
        if not self.test_active or self.test_finished:
            return "break"
        # Start the timer only for actual text input, not modifier/navigation keys.
        if not self.has_started_typing and event.char and event.char.isprintable():
            self.has_started_typing = True
            self.started_at = time.perf_counter()
            self._schedule_timer()
        return None

    def _on_key_release(self, event=None):
        if not self.test_active or self.test_finished:
            return
        typed = self.typing_box.get("1.0", "end-1c")
        self._update_feedback(typed)
        self._update_live_stats(typed)

        # Automatically finish when the full sentence has been entered.
        if typed == self.current_sentence:
            self.finish_test(auto_finished=True)

    def _on_paste(self, event=None):
        # The standard Text paste binding is retained. Refresh after Tk processes it.
        self.after(10, self._on_key_release)

    def _schedule_timer(self):
        self._cancel_timer()
        self._tick_timer()

    def _tick_timer(self):
        if not self.test_active or self.test_finished or self.started_at is None:
            return
        self.elapsed = max(0.0, time.perf_counter() - self.started_at)
        typed = self.typing_box.get("1.0", "end-1c")
        self._update_live_stats(typed)
        self.timer_job = self.after(200, self._tick_timer)

    def _cancel_timer(self):
        if self.timer_job is not None:
            try:
                self.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None

    def _update_feedback(self, typed):
        self.typing_box.tag_remove("correct", "1.0", "end")
        self.typing_box.tag_remove("incorrect", "1.0", "end")
        self.typing_box.tag_remove("normal", "1.0", "end")

        for i, char in enumerate(typed):
            start = f"1.0+{i}c"
            end = f"1.0+{i + 1}c"
            if i < len(self.current_sentence) and char == self.current_sentence[i]:
                self.typing_box.tag_add("correct", start, end)
            else:
                self.typing_box.tag_add("incorrect", start, end)

        self.char_count_label.configure(
            text=f"{len(typed)} character" + ("" if len(typed) == 1 else "s")
        )

    def _calculate(self, typed, elapsed):
        original = self.current_sentence
        correct = sum(
            1 for i in range(min(len(original), len(typed)))
            if original[i] == typed[i]
        )
        # Missing and extra characters are treated as incorrect.
        denominator = max(len(original), len(typed))
        accuracy = (correct / denominator * 100) if denominator else 0.0
        accuracy = min(100.0, max(0.0, accuracy))
        words = len(typed.split())
        wpm = (words / (elapsed / 60.0)) if elapsed > 0 else 0.0
        return words, wpm, accuracy, correct

    def _update_live_stats(self, typed):
        if self.started_at is not None and self.test_active and not self.test_finished:
            self.elapsed = max(0.0, time.perf_counter() - self.started_at)
        words, wpm, accuracy, _ = self._calculate(typed, self.elapsed)
        self.last_wpm = wpm
        self.last_accuracy = accuracy
        self._refresh_stats(words, wpm, accuracy)

    def _refresh_stats(self, words=0, wpm=0.0, accuracy=100.0):
        total_seconds = int(self.elapsed)
        minutes, seconds = divmod(total_seconds, 60)
        self.time_value.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.wpm_value.configure(text=f"{wpm:.1f}")
        self.accuracy_value.configure(text=f"{accuracy:.1f}%")

    def finish_test(self, auto_finished=False):
        if not self.test_active or self.test_finished:
            return

        typed = self.typing_box.get("1.0", "end-1c")
        if not typed.strip():
            self._set_status("Type at least one character before finishing.", RED)
            self.typing_box.focus_set()
            return

        if self.started_at is not None:
            self.elapsed = max(0.0, time.perf_counter() - self.started_at)
        else:
            self.elapsed = 0.0

        self.test_finished = True
        self.test_active = False
        self._cancel_timer()
        self._set_typing_enabled(False)

        words, wpm, accuracy, correct = self._calculate(typed, self.elapsed)
        self.last_wpm = wpm
        self.last_accuracy = accuracy
        self._refresh_stats(words, wpm, accuracy)

        self.start_button.configure(state="normal")
        self.finish_button.configure(state="disabled")
        self.retry_button.configure(state="normal")

        if auto_finished:
            message = "Sentence completed! Great work."
        else:
            message = "Test finished. Try again to practise another sentence."
        self._set_status(message, GREEN)

        missing = max(0, len(self.current_sentence) - len(typed))
        extra = max(0, len(typed) - len(self.current_sentence))
        self.feedback_label.configure(
            text=f"Results  •  {words} words  •  {correct}/{len(self.current_sentence)} matching characters  •  {missing} missing  •  {extra} extra",
            text_color=GREEN if accuracy >= 90 else MUTED,
        )

    def destroy(self):
        self._cancel_timer()
        super().destroy()


if __name__ == "__main__":
    app = TypeFlowApp()
    app.mainloop()
