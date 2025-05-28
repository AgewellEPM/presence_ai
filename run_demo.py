# presence_ai/run_demo.py

import argparse
import os
import atexit
import shutil # For teardown_ram_scratch

from config.config import Config
from ere_core.ere_engine import EREEngine
from virem_vault.auth_layer import AuthLayer
from virem_vault.driver import VIREMVaultDriver
from virem_vault.scratchpad import ScratchpadVault

# --- Conceptual Session Lifetime & RAM Teardown ---
RAM_SCRATCH_PATH = "scratch_memory"

def initialize_ram_scratch():
    # Simulate RAM usage by creating a temp folder (not saved on reboot)
    os.makedirs(RAM_SCRATCH_PATH, exist_ok=True)
    print(f"RAM scratch directory initialized at: {RAM_SCRATCH_PATH}")

def teardown_ram_scratch():
    if os.path.exists(RAM_SCRATCH_PATH):
        shutil.rmtree(RAM_SCRATCH_PATH, ignore_errors=True)
        print(f"RAM scratch directory '{RAM_SCRATCH_PATH}' torn down.")

# Hook teardown to session exit
atexit.register(teardown_ram_scratch)
# --- End of Conceptual Teardown ---


def main():
    # Load configuration
    app_config = Config() # Config is now a singleton loaded via config.json

    parser = argparse.ArgumentParser(description="Run Stateless AI with Affective Soft Memory.")
    parser.add_argument("--mode", type=str, default=app_config.DEFAULT_MODE, choices=["scratch", "persistent"],
                        help=f"Operating mode: 'scratch' (RAM-only) or 'persistent' (ChaCha20 encrypted file-based). Default: {app_config.DEFAULT_MODE}")
    args = parser.parse_args()

    print(f"--- Starting Stateless AI Demo in {args.mode.upper()} Mode ---")

    if args.mode == "scratch":
        initialize_ram_scratch() # Initialize conceptual RAM scratchpad

    # 1. Authentication Layer (Mock for now)
    auth_layer = AuthLayer()
    if not auth_layer.authenticate(mode=args.mode):
        print("Authentication failed. Exiting.")
        return

    # 2. VIREM Vault Initialization
    if args.mode == "scratch":
        virem_vault = ScratchpadVault()
        print("VIREM Vault: Using RAM-only Scratchpad.")
    else: # persistent
        virem_vault = VIREMVaultDriver(vault_path=app_config.VAULT_PATH) # Note: VAULT_PATH from Config is now derived from vault_key_path
        print(f"VIREM Vault: Using persistent encrypted vault at {app_config.VAULT_PATH}.")

    # 3. Emotive Resonance Engine Initialization
    ere_engine = EREEngine() # ERE will now use emotion_parser for detection
    print("ERE Engine: Initialized for affective resonance.")

    # Main interaction loop (simplified)
    print("\nAI is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting session. All ephemeral memory cleared (and RAM scratchpad torn down).")
            # In persistent mode, the vault driver might clear its file on exit
            if args.mode == "persistent":
                virem_vault.clear_vault()
            elif args.mode == "scratch":
                virem_vault.clear_session_memory() # Explicitly clear scratchpad data
            break

        # Simulate processing:
        # 1. Detect emotion from user_input (ERE's job)
        detected_emotion = ere_engine.detect_emotion(user_input) # Now uses emotion_parser internally
        print(f"(Debug: Detected emotion: {detected_emotion})")

        # 2. Adjust ERE pathway weights based on detected emotion
        ere_engine.adjust_pathway_weights(detected_emotion)

        # 3. Generate response based on current ERE state and soft memory biases
        ai_response = ere_engine.generate_response(user_input, current_emotion=detected_emotion)
        print(f"AI: {ai_response}")

        # In persistent mode, the vault driver might periodically sync blocks
        if args.mode == "persistent":
            # Example: Simulate ephemeral memory interaction via vault
            # This is NOT storing user data, but perhaps ephemeral "session context"
            # that's then immediately encrypted and decayed or overwritten.
            virem_vault.store_block(f"context_marker_{hash(user_input)}", f"Processed input for {detected_emotion}")


if __name__ == "__main__":
    main()
