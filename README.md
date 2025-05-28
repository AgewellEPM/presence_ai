# Stateless AI with Affective Soft Memory (Project Name: Presence AI)

This project explores a revolutionary model for AI personalization and learning that prioritizes user privacy. It leverages a **Stateless AI with Affective Soft Memory**, powered by the **Emotive Resonance Engine (ERE)** and the **VIREM Vault (Vault for Identity-Rooted Ephemeral Memory)**.

## Core Concepts

* **Stateless:** No explicit user data, conversation history, or personal identifiable information is persistently stored. Each session begins as a blank slate.
* **Affective Soft Memory:** Instead of storing facts, the ERE adjusts internal "pathway weights" based on emotional resonance encountered during interactions. This creates a dynamic, mood-adjusted behavioral model.
* **Behavioral Adaptation Without Recall:** The AI doesn't remember *what* you said, but adjusts *how it responds* next time, learning by emotional resonance rather than data retention.
* **Ephemeral Memory (VIREM Vault):** For necessary short-term contextual understanding within a session, an ephemeral, highly secure, and transient memory vault is utilized, which is designed to decay or be fully cleared.

## Project Structure

(Refer to the detailed file structure in the project directory for a complete overview.)

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd presence_ai
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the demo:**
    * **Stateless (RAM-only) Mode:**
        ```bash
        python run_demo.py --mode scratch
        ```
    * **Encrypted Persistent (Ephemeral) Mode:**
        ```bash
        python run_demo.py --mode persistent
        ```

## Modules

* **`ere_core/`**: Contains the Emotive Resonance Engine logic.
* **`virem_vault/`**: Manages ephemeral memory and secure access.
* **`config/`**: Project configuration settings.
* **`logs/`**: Optional logging for internal AI states (not user data).
* **`vault_data/`**: Stores encrypted blocks in `persistent` mode (if enabled).
* **`scratch_memory/`**: Conceptual directory for RAM-only ephemeral data.

## Contribution

(Add details on how to contribute if this is an open-source project.)
