class FlashcardEngine:

    def __init__(self, flashcards):
        self.flashcards = flashcards
        self.current_card = 0
        self.revealed = False
        self.known_cards = []
        self.practice_cards = []

    # --------------------------------------------
    # Get current flashcard
    # --------------------------------------------

    def get_current_card(self):

        if self.current_card >= len(self.flashcards):
            return None

        return self.flashcards[self.current_card]

    # --------------------------------------------
    # Reveal answer
    # --------------------------------------------

    def reveal_answer(self):

        self.revealed = True

        return self.get_current_card()

    # --------------------------------------------
    # Mark card as known
    # --------------------------------------------

    def mark_known(self):

        card = self.get_current_card()

        if card is not None:

            self.known_cards.append(
                self.current_card
            )

        return self.next_card()

    # --------------------------------------------
    # Mark card for practice
    # --------------------------------------------

    def mark_for_practice(self):

        card = self.get_current_card()

        if card is not None:

            self.practice_cards.append(
                self.current_card
            )

        return self.next_card()

    # --------------------------------------------
    # Move to next card
    # --------------------------------------------

    def next_card(self):

        if self.current_card < len(self.flashcards) - 1:

            self.current_card += 1

            self.revealed = False

            return True

        # No more cards
        self.current_card = len(
            self.flashcards
        )

        return False

    # --------------------------------------------
    # Check completion
    # --------------------------------------------

    def is_complete(self):

        return (
            self.current_card >= len(
                self.flashcards
            )
        )

    # --------------------------------------------
    # Progress
    # --------------------------------------------

    def get_total_cards(self):

        return len(self.flashcards)

    def get_known_count(self):

        return len(self.known_cards)

    def get_practice_count(self):

        return len(self.practice_cards)

    def get_progress_percentage(self):

        if len(self.flashcards) == 0:
            return 0

        completed = (
            len(self.known_cards)
            + len(self.practice_cards)
        )

        return (
            completed
            / len(self.flashcards)
        ) * 100