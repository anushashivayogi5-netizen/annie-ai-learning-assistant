import streamlit as st
import os
import json

from document_manager import process_document
from gemini_service import ask_ai, reset_chat
from quiz_engine import QuizEngine
from quiz_service import generate_quiz
from rag_service import generate_rag_answer, retrieve_relevant_chunks
from flashcard_service import generate_flashcards
from flashcard_engine import FlashcardEngine

UPLOAD_DIR = "uploaded_documents"
PROGRESS_FILE = "learning_progress.json"
def save_learning_progress():
    progress = {
        "quiz_history": st.session_state.quiz_history,
        "flashcard_history": st.session_state.flashcard_history
    }

    with open(PROGRESS_FILE, "w") as f:
        json.dump(
            progress,
            f,
            indent=4
        )

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)
# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# Initialize session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document" not in st.session_state:
    st.session_state.document = None

    # --------------------------------------------------
    # Restore document after refresh
    # --------------------------------------------------

    if st.session_state.document is None:

        saved_files = os.listdir(UPLOAD_DIR)

        if saved_files:
            saved_file = saved_files[0]

            saved_path = os.path.join(
                UPLOAD_DIR,
                saved_file
            )

            with open(saved_path, "rb") as f:
                with st.spinner(
                        "Restoring learning material..."
                ):
                    document = process_document(f)

                    document["filename"] = saved_file

                    st.session_state.document = document
    # --------------------------------------------------
    # Restore saved document after browser refresh
    # --------------------------------------------------

    if st.session_state.document is None:

        saved_files = os.listdir(UPLOAD_DIR)

        if saved_files:
            saved_file = saved_files[0]

            saved_path = os.path.join(
                UPLOAD_DIR,
                saved_file
            )

            with open(saved_path, "rb") as f:
                with st.spinner(
                        "Restoring your learning material..."
                ):
                    document = process_document(f)

                    document["filename"] = saved_file

                    st.session_state.document = document

if "current_page" not in st.session_state:
    st.session_state.current_page = "chat"

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "quiz_engine" not in st.session_state:
    st.session_state.quiz_engine = None

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

if "quiz_question_results" not in st.session_state:
    st.session_state.quiz_question_results = []

if "quiz_question_results" not in st.session_state:
    st.session_state.quiz_question_results = []

if "flashcards" not in st.session_state:
        st.session_state.flashcards = None

if "flashcard_engine" not in st.session_state:
        st.session_state.flashcard_engine = None

# --------------------------------------------------
# Load saved learning progress
# --------------------------------------------------

if os.path.exists(PROGRESS_FILE):

    with open(PROGRESS_FILE, "r") as f:

        saved_progress = json.load(f)

else:

    saved_progress = {
        "quiz_history": [],
        "flashcard_history": []
    }


if "quiz_history" not in st.session_state:

    st.session_state.quiz_history = (
        saved_progress["quiz_history"]
    )


if "flashcard_history" not in st.session_state:

    st.session_state.flashcard_history = (
        saved_progress["flashcard_history"]
    )
# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("🎓 Learning Assistant")

    st.write("Your personal AI tutor")

    st.divider()

    st.subheader("Learning Tools")

    # Navigation buttons

    if st.button("💬 Chat", use_container_width=True):
        st.session_state.current_page = "chat"
        st.rerun()

    if st.button("📄 Documents", use_container_width=True):
        st.session_state.current_page = "documents"
        st.rerun()

    if st.button("📝 Quizzes", use_container_width=True):
        st.session_state.current_page = "quiz"
        st.rerun()

    if st.button("🃏 Flashcards", use_container_width=True):
        st.session_state.current_page = "flashcards"
        st.rerun()

    if st.button("📊 Progress", use_container_width=True):
        st.session_state.current_page = "progress"
        st.rerun()

    st.divider()

    # --------------------------------------------------
    # PDF Upload
    # --------------------------------------------------

    st.subheader("📄 Upload Learning Material")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        saved_path = os.path.join(

            UPLOAD_DIR,

            uploaded_file.name

        )

        with open(saved_path, "wb") as f:

            f.write(uploaded_file.getbuffer())
        if (
            st.session_state.document is None
            or st.session_state.document.get("filename")
            != uploaded_file.name
        ):

            with st.spinner(
                "Processing your document..."
            ):

                document = process_document(
                    uploaded_file
                )

                document["filename"] = uploaded_file.name

                st.session_state.document = document

                # Reset chat
                st.session_state.messages = []

                # Reset quiz
                st.session_state.flashcards = None
                st.session_state.flashcard_engine = None

                reset_chat()

            st.success(
                f"Loaded: {uploaded_file.name}"
            )

    # --------------------------------------------------
    # Current document
    # --------------------------------------------------

    if st.session_state.document is not None:

        document = st.session_state.document

        st.divider()

        st.subheader("📚 Current Document")

        st.write(
            document["filename"]
        )

        st.caption(
            f"{len(document['chunks'])} chunks indexed"
        )

    # --------------------------------------------------
    # Clear conversation
    # --------------------------------------------------

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        reset_chat()

        st.rerun()


# ==================================================
# CHAT PAGE
# ==================================================

if st.session_state.current_page == "chat":

    st.title("🎓 AI Learning Assistant")

    if st.session_state.document is not None:

        st.caption(
            "Ask questions about your uploaded learning material."
        )

    else:

        st.caption(
            "Ask your AI tutor anything you're learning."
        )

    # ----------------------------------------------
    # Conversation history
    # ----------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):

                st.markdown("### 📚 Sources")

                displayed_pages = set()

                for source in message["sources"]:

                    page_number = source["page_number"]

                    if page_number not in displayed_pages:

                        st.markdown(
                            f"📄 **Page {page_number}**"
                        )

                        displayed_pages.add(
                            page_number
                        )

    # ----------------------------------------------
    # Chat input
    # ----------------------------------------------

    user_message = st.chat_input(
        "Ask your AI tutor anything..."
    )

    if user_message:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        with st.chat_message("user"):

            st.markdown(
                user_message
            )

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    if st.session_state.document is not None:

                        document = (
                            st.session_state.document
                        )

                        answer, retrieved_chunks = (
                            generate_rag_answer(
                                user_message,
                                document["chunks"],
                                document["index"],
                                top_k=3
                            )
                        )

                        sources = retrieved_chunks

                    else:

                        answer = ask_ai(
                            user_message
                        )

                        sources = []

                    st.markdown(answer)

                    if sources:

                        st.markdown("### 📚 Sources")

                        displayed_pages = set()

                        for source in sources:

                            page_number = source[
                                "page_number"
                            ]

                            if page_number not in displayed_pages:

                                st.markdown(
                                    f"📄 **Page {page_number}**"
                                )

                                displayed_pages.add(
                                    page_number
                                )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# ==================================================
# DOCUMENTS PAGE
# ==================================================

elif st.session_state.current_page == "documents":

    st.title("📄 Documents")

    st.write(
        "Upload and manage your learning materials."
    )

    if st.session_state.document is None:

        st.info(
            "Upload a PDF using the sidebar to get started."
        )

    else:

        document = st.session_state.document

        st.success(
            f"📚 {document['filename']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Pages",
                len(document["pages"])
            )

        with col2:
            st.metric(
                "Chunks",
                len(document["chunks"])
            )

        with col3:
            st.metric(
                "Embeddings",
                len(document["embeddings"])
            )

        st.divider()

        st.subheader("Document Ready")

        st.write(
            "Your document has been processed and "
            "is ready for Chat and Quiz generation."
        )


# ==================================================
# QUIZ PAGE
# ==================================================

elif st.session_state.current_page == "quiz":

    st.title("📝 AI Quiz Generator")

    if st.session_state.document is None:

        st.warning(
            "Please upload a PDF before generating a quiz."
        )

    else:

        document = st.session_state.document

        st.write(
            f"Create a quiz from **{document['filename']}**"
        )

        st.divider()

        # ------------------------------------------
        # Quiz settings
        # ------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            num_questions = st.selectbox(
                "Number of questions",
                [3, 5, 10],
                index=1
            )

        with col2:

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ]
            )

        # ------------------------------------------
        # Generate quiz
        # ------------------------------------------

        if st.button(
            "🚀 Generate Quiz",
            use_container_width=True
        ):

            with st.spinner(
                "Creating your quiz..."
            ):

                try:

                    # Retrieve relevant document content
                    relevant_chunks = (
                        retrieve_relevant_chunks(
                            "Create a quiz covering the important concepts in this document.",
                            document["chunks"],
                            document["index"],
                            top_k=8
                        )
                    )

                    # Build context
                    context_parts = []

                    for chunk in relevant_chunks:

                        context_parts.append(
                            f"[Page {chunk['page_number']}]\n"
                            f"{chunk['text']}"
                        )

                    context = "\n\n".join(
                        context_parts
                    )

                    # Generate quiz
                    quiz = generate_quiz(
                        context,
                        num_questions=num_questions,
                        difficulty=difficulty
                    )

                    # Create quiz engine
                    st.session_state.quiz = quiz

                    st.session_state.quiz_engine = (
                        QuizEngine(quiz)
                    )

                    st.session_state.quiz_result = None

                    st.session_state.quiz_question_results = []

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Could not generate quiz: {e}"
                    )

        # ------------------------------------------
        # Display quiz
        # ------------------------------------------

        if (
            st.session_state.quiz_engine is not None
        ):

            engine = (
                st.session_state.quiz_engine
            )

            question = (
                engine.get_current_question()
            )

            # --------------------------------------
            # Quiz complete
            # --------------------------------------

            if engine.is_complete():

                score = engine.get_score()

                total = (
                    engine.get_total_questions()
                )

                percentage = (
                    engine.get_percentage()
                )
                # Save quiz result
                # Save quiz result once
                if (
                        not st.session_state.quiz_history
                        or st.session_state.quiz_history[-1]["quiz_id"]
                        != id(engine)
                ):
                    st.session_state.quiz_history.append(
                        {
                            "quiz_id": id(engine),
                            "score": score,
                            "total": total,
                            "percentage": percentage,
                            "question_results": (
                                st.session_state.quiz_question_results
                            )
                        }
                    )

                    save_learning_progress()

                    save_learning_progress()
                st.success(
                    "🎉 Quiz Complete!"
                )

                st.metric(
                    "Your Score",
                    f"{score} / {total}"
                )

                st.metric(
                    "Percentage",
                    f"{percentage:.0f}%"
                )

                if percentage >= 80:

                    st.balloons()

                    st.success(
                        "🌟 Excellent work!"
                    )

                elif percentage >= 60:

                    st.info(
                        "👍 Good job! Keep practicing."
                    )

                else:

                    st.warning(
                        "💪 Keep learning and try again!"
                    )

                if st.button(
                    "🔄 Take Quiz Again",
                    use_container_width=True
                ):

                    st.session_state.quiz_engine = (
                        QuizEngine(
                            st.session_state.quiz
                        )
                    )

                    st.session_state.quiz_result = None

                    st.session_state.quiz_question_results = []

                    st.rerun()

            # --------------------------------------
            # Current question
            # --------------------------------------

            else:

                question_number = (
                    engine.current_question + 1
                )

                total_questions = (
                    engine.get_total_questions()
                )

                st.subheader(
                    f"Question {question_number} "
                    f"of {total_questions}"
                )

                st.progress(
                    question_number / total_questions
                )

                st.markdown(
                    f"### {question['question']}"
                )


                selected_answer = st.radio(
                    "Choose your answer:",
                    question["options"],
                    key=f"question_{question_number}"
                )

                # ----------------------------------
                # Submit answer
                # ----------------------------------

                if not engine.answered:

                    if st.button(
                        "✅ Submit Answer",
                        use_container_width=True
                    ):

                        result = (
                            engine.submit_answer(
                                selected_answer
                            )
                        )

                        st.session_state.quiz_result = (
                            result
                        )

                        st.session_state.quiz_question_results.append(
                            {
                                "topic": question.get(
                                    "topic",
                                    f"Page {result.get('page_number', 'Unknown')}"
                                ),
                                "is_correct": result["is_correct"]
                            }
                        )

                        st.rerun()

                # ----------------------------------
                # Show result
                # ----------------------------------

                else:

                    result = (
                        st.session_state.quiz_result
                    )

                    if result["is_correct"]:

                        st.success(
                            "✅ Correct!"
                        )

                    else:

                        st.error(
                            "❌ Incorrect"
                        )

                        st.write(
                            f"**Correct answer:** "
                            f"{result['correct_answer']}"
                        )

                    st.info(
                        f"💡 {result['explanation']}"
                    )

                    st.caption(
                        f"📄 Source: Page "
                        f"{result['page_number']}"
                    )

                    # ----------------------------------
                    # Next question
                    # ----------------------------------

                    if st.button(
                        "➡️ Next Question",
                        use_container_width=True
                    ):

                        engine.next_question()

                        st.session_state.quiz_result = None

                        st.rerun()


# ==================================================
# FLASHCARDS PAGE
# ==================================================

elif st.session_state.current_page == "flashcards":

    st.title("🃏 Flashcards")

    if st.session_state.document is None:

        st.warning(
            "Please upload a PDF before generating flashcards."
        )

    else:

        document = st.session_state.document

        st.write(
            f"Create flashcards from "
            f"**{document['filename']}**"
        )

        st.divider()

        # ------------------------------------------
        # Flashcard settings
        # ------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            num_cards = st.selectbox(
                "Number of flashcards",
                [3, 5, 10],
                index=1
            )

        with col2:

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ]
            )

        # ------------------------------------------
        # Generate flashcards
        # ------------------------------------------

        if st.session_state.flashcard_engine is None:

            if st.button(
                "🚀 Generate Flashcards",
                use_container_width=True
            ):

                with st.spinner(
                    "Creating your flashcards..."
                ):

                    try:

                        # Retrieve relevant content
                        relevant_chunks = (
                            retrieve_relevant_chunks(
                                "Create flashcards covering the important concepts in this document.",
                                document["chunks"],
                                document["index"],
                                top_k=8
                            )
                        )

                        # Build context
                        context_parts = []

                        for chunk in relevant_chunks:

                            context_parts.append(
                                f"[Page {chunk['page_number']}]\n"
                                f"{chunk['text']}"
                            )

                        context = "\n\n".join(
                            context_parts
                        )

                        # Generate flashcards
                        flashcards = generate_flashcards(
                            context,
                            num_cards=num_cards,
                            difficulty=difficulty
                        )

                        # Create flashcard engine
                        st.session_state.flashcards = (
                            flashcards
                        )

                        st.session_state.flashcard_engine = (
                            FlashcardEngine(
                                flashcards
                            )
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not generate flashcards: {e}"
                        )

        # ------------------------------------------
        # Flashcard experience
        # ------------------------------------------

        else:

            engine = (
                st.session_state.flashcard_engine
            )

            # --------------------------------------
            # Completed
            # --------------------------------------

            if engine.is_complete():

                total = (
                    engine.get_total_cards()
                )

                known = (
                    engine.get_known_count()
                )

                practice = (
                    engine.get_practice_count()
                )

                # Save flashcard result
                if not st.session_state.flashcard_history or \
                        st.session_state.flashcard_history[-1]["session_id"] != id(engine):
                    st.session_state.flashcard_history.append(
                        {
                            "session_id": id(engine),
                            "total": total,
                            "known": known,
                            "practice": practice
                        }
                    )
                save_learning_progress()

                st.success(
                    "🎉 Flashcards Complete!"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Cards Reviewed",
                        total
                    )

                with col2:

                    st.metric(
                        "✅ I Know This",
                        known
                    )

                with col3:

                    st.metric(
                        "😕 Need Practice",
                        practice
                    )

                st.progress(1.0)

                st.write(
                    f"**100% completed**"
                )

                if st.button(
                    "🔄 Review Again",
                    use_container_width=True
                ):

                    st.session_state.flashcard_engine = (
                        FlashcardEngine(
                            st.session_state.flashcards
                        )
                    )

                    st.rerun()

            # --------------------------------------
            # Current card
            # --------------------------------------

            else:

                card_number = (
                    engine.current_card + 1
                )

                total_cards = (
                    engine.get_total_cards()
                )

                st.subheader(
                    f"Flashcard {card_number} "
                    f"of {total_cards}"
                )

                st.progress(
                    card_number / total_cards
                )

                card = (
                    engine.get_current_card()
                )

                # ----------------------------------
                # Card front
                # ----------------------------------

                st.markdown(
                    "### 💭 Question / Concept"
                )

                st.info(
                    card["front"]
                )

                # ----------------------------------
                # Reveal answer
                # ----------------------------------

                if not engine.revealed:

                    if st.button(
                        "👆 Reveal Answer",
                        use_container_width=True
                    ):

                        engine.reveal_answer()

                        st.rerun()

                # ----------------------------------
                # Show answer
                # ----------------------------------

                else:

                    st.markdown(
                        "### 💡 Answer"
                    )

                    st.success(
                        card["back"]
                    )

                    st.caption(
                        f"📄 Source: Page "
                        f"{card['page_number']}"
                    )

                    st.divider()

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "😕 Need Practice",
                            use_container_width=True
                        ):

                            engine.mark_for_practice()

                            st.rerun()

                    with col2:

                        if st.button(
                            "✅ I Know This",
                            use_container_width=True
                        ):

                            engine.mark_known()

                            st.rerun()

# ==================================================
# PROGRESS PAGE
# ==================================================

elif st.session_state.current_page == "progress":

    st.title("📊 Learning Progress")

    st.caption(
        "Track your learning activity and performance."
    )

    # ------------------------------------------
    # Check if a document is loaded
    # ------------------------------------------

    if st.session_state.document is None:

        st.info(
            "Upload a learning document to start "
            "tracking your progress."
        )

    else:

        document = st.session_state.document

        # ------------------------------------------
        # Current document
        # ------------------------------------------

        st.subheader("📚 Current Learning Material")

        st.success(
            document["filename"]
        )

        st.divider()

        # ------------------------------------------
        # Quiz Performance
        # ------------------------------------------

        st.subheader("📝 Quiz Performance")

        if st.session_state.quiz_history:

            latest_quiz = (
                st.session_state.quiz_history[-1]
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Latest Score",
                    f"{latest_quiz['score']}/"
                    f"{latest_quiz['total']}"
                )

            with col2:

                st.metric(
                    "Accuracy",
                    f"{latest_quiz['percentage']:.0f}%"
                )

            with col3:

                if latest_quiz["percentage"] >= 80:
                    status = "🌟 Excellent"

                elif latest_quiz["percentage"] >= 60:
                    status = "👍 Good"

                else:
                    status = "💪 Keep Practicing"

                st.metric(
                    "Status",
                    status
                )

        else:

            st.info(
                "Complete a quiz to see your performance."
            )

        st.divider()

        # ------------------------------------------
        # Flashcard Performance
        # ------------------------------------------

        st.subheader("🃏 Flashcard Progress")

        if st.session_state.flashcard_history:

            latest_flashcards = (
                st.session_state.flashcard_history[-1]
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Cards Reviewed",
                    latest_flashcards["total"]
                )

            with col2:

                st.metric(
                    "✅ I Know This",
                    latest_flashcards["known"]
                )

            with col3:

                st.metric(
                    "😕 Need Practice",
                    latest_flashcards["practice"]
                )

        else:

            st.info(
                "Complete some flashcards to see "
                "your progress."
            )

        st.divider()

        # ------------------------------------------
        # Learning Activity
        # ------------------------------------------

        st.subheader("🎯 Learning Activity")

        quiz_completed = len(
            st.session_state.quiz_history
        )

        flashcard_sessions = len(
            st.session_state.flashcard_history
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📝 Quizzes Completed",
                quiz_completed
            )

        with col2:

            st.metric(
                "🃏 Flashcard Sessions",
                flashcard_sessions
            )

        st.divider()

        # ------------------------------------------
        # Learning Summary
        # ------------------------------------------

        st.subheader("📈 Learning Summary")

        if (
            st.session_state.quiz_history
            or st.session_state.flashcard_history
        ):

            st.success(
                "🎉 You are actively learning! "
                "Keep practicing to improve your mastery."
            )

            if st.session_state.quiz_history:

                best_score = max(
                    quiz["percentage"]
                    for quiz
                    in st.session_state.quiz_history
                )

                st.write(
                    f"🏆 Best quiz score: "
                    f"**{best_score:.0f}%**"
                )

            if st.session_state.flashcard_history:

                total_known = sum(
                    session["known"]
                    for session
                    in st.session_state.flashcard_history
                )

                total_practice = sum(
                    session["practice"]
                    for session
                    in st.session_state.flashcard_history
                )

                st.write(
                    f"✅ Cards mastered: "
                    f"**{total_known}**"
                )

                st.write(
                    f"📖 Cards needing practice: "
                    f"**{total_practice}**"
                )

        else:

            st.info(
                "Your learning statistics will appear here "
                "after you complete quizzes or flashcards."
            )

        # --------------------------------------------------
        # Personalized Learning Recommendations
        # --------------------------------------------------

        st.divider()

        st.header("🎯 Personalized Learning Recommendations")

        quiz_history = st.session_state.quiz_history
        flashcard_history = st.session_state.flashcard_history

        # --------------------------------------------------
        # Calculate current learning performance
        # --------------------------------------------------

        if quiz_history:

            best_quiz_score = max(
                quiz["percentage"]
                for quiz in quiz_history
            )

        else:

            best_quiz_score = 0

        if flashcard_history:

            total_practice = sum(
                session["practice"]
                for session in flashcard_history
            )

            total_known = sum(
                session["known"]
                for session in flashcard_history
            )

        else:

            total_practice = 0
            total_known = 0

        # --------------------------------------------------
        # Generate personalized recommendations
        # --------------------------------------------------

        recommendations = []

        # Quiz recommendation
        if quiz_history:

            if best_quiz_score < 50:

                recommendations.append(
                    "📚 Your quiz score is below 50%. "
                    "Review the learning material and focus "
                    "on the core concepts before taking another quiz."
                )

            elif best_quiz_score < 80:

                recommendations.append(
                    "📖 You're making progress! "
                    "Review the topics you missed and take "
                    "another quiz to strengthen your understanding."
                )

            else:

                recommendations.append(
                    "🌟 Excellent quiz performance! "
                    "You have a strong understanding of the material. "
                    "Try a harder quiz next."
                )

        # Flashcard recommendation
        if total_practice > 0:
            recommendations.append(
                f"🃏 You have {total_practice} flashcards "
                "that need practice. Review these cards again "
                "before moving to new topics."
            )

        if total_known > 0:
            recommendations.append(
                f"✅ You have mastered {total_known} flashcards. "
                "Keep reviewing them periodically to retain "
                "what you've learned."
            )

        # General recommendation
        if quiz_history and flashcard_history:
            recommendations.append(
                "🚀 Keep using both quizzes and flashcards. "
                "Quizzes test your understanding, while "
                "flashcards help strengthen memory."
            )

        # --------------------------------------------------
        # Display recommendations
        # --------------------------------------------------

        if recommendations:

            for recommendation in recommendations:
                st.info(
                    recommendation
                )

        else:

            st.info(
                "Complete a quiz or flashcard session "
                "to receive personalized recommendations."
            )

        # --------------------------------------------------
        # Topic-Level Learning Analysis
        # --------------------------------------------------

        st.divider()

        st.header("🎯 Topic-Level Learning Analysis")

        topic_stats = {}

        for quiz in quiz_history:

            for answer in quiz.get(
                "question_results",
                []
            ):

                topic = answer["topic"]

                if topic.startswith("Page "):
                    continue

                if topic not in topic_stats:

                    topic_stats[topic] = {
                        "correct": 0,
                        "total": 0
                    }

                topic_stats[topic]["total"] += 1

                if answer["is_correct"]:

                    topic_stats[topic]["correct"] += 1


        if topic_stats:

            weakest_topic = min(
                topic_stats,
                key=lambda topic: (
                    topic_stats[topic]["correct"]
                    / topic_stats[topic]["total"]
                )
            )

            weakest = topic_stats[weakest_topic]

            st.warning(
                f"📚 Focus area: **{weakest_topic}**. "
                f"You answered {weakest['correct']} out of "
                f"{weakest['total']} question(s) correctly."
            )

            st.subheader("🚀 Your Personalized Study Plan")

            st.write(
                f"1. 📖 Review the material from "
                f"**{weakest_topic}**."
            )

            st.write(
                "2. 🃏 Review flashcards marked "
                "**Need Practice**."
            )

            st.write(
                "3. 📝 Take another quiz to improve "
                "this focus area."
            )

        else:

            st.info(
                "Complete one new quiz to unlock "
                "topic-level learning analysis."
            )