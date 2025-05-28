# presence_ai/run_demo.py (Updated section)

import argparse
import os
import atexit
import shutil

from config.config import Config
from ere_core.ere_engine import EREEngine
from virem_vault.auth_layer import AuthLayer
from virem_vault.driver import VIREMVaultDriver
from virem_vault.scratchpad import ScratchpadVault
from ere_core.loop_consciousness import LoopConsciousness
from ere_core.reaction_mapper import ReactionMapper # NEW IMPORT

# --- Conceptual Session Lifetime & RAM Teardown ---
RAM_SCRATCH_PATH = "scratch_memory"

def initialize_ram_scratch():
    os.makedirs(RAM_SCRATCH_PATH, exist_ok=True)
    print(f"RAM scratch directory initialized at: {RAM_SCRATCH_PATH}")

def teardown_ram_scratch():
    if os.path.exists(RAM_SCRATCH_PATH):
        shutil.rmtree(RAM_SCRATCH_PATH, ignore_errors=True)
        print(f"RAM scratch directory '{RAM_SCRATCH_PATH}' torn down.")

atexit.register(teardown_ram_scratch)
# --- End of Conceptual Teardown ---


def main():
    app_config = Config()

    parser = argparse.ArgumentParser(description="Run Stateless AI with Affective Soft Memory.")
    parser.add_argument("--mode", type=str, default=app_config.DEFAULT_MODE, choices=["scratch", "persistent"],
                        help=f"Operating mode: 'scratch' (RAM-only) or 'persistent' (ChaCha20 encrypted file-based). Default: {app_config.DEFAULT_MODE}")
    args = parser.parse_args()

    print(f"--- Starting Stateless AI Demo in {args.mode.upper()} Mode ---")

    if args.mode == "scratch":
        initialize_ram_scratch()

    auth_layer = AuthLayer()
    if not auth_layer.authenticate(mode=args.mode):
        print("Authentication failed. Exiting.")
        return

    if args.mode == "scratch":
        virem_vault = ScratchpadVault()
        print("VIREM Vault: Using RAM-only Scratchpad.")
    else: # persistent
        virem_vault = VIREMVaultDriver(vault_path=app_config.VAULT_PATH)
        print(f"VIREM Vault: Using persistent encrypted vault at {app_config.VAULT_PATH}.")

    ere_engine = EREEngine()
    print("ERE Engine: Initialized for affective resonance.")

    consciousness_loop = LoopConsciousness(heartbeat_interval=3.0, memory_capacity=5)
    print("Consciousness loop initialized.")

    reaction_mapper = ReactionMapper() # NEW: Initialize ReactionMapper
    print("Reaction mapper initialized.")


    print("\nAI is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting session. All ephemeral memory cleared (and RAM scratchpad torn down).")
            if args.mode == "persistent":
                virem_vault.clear_vault()
            elif args.mode == "scratch":
                virem_vault.clear_session_memory()
            break

        detected_emotion = ere_engine.detect_emotion(user_input)
        print(f"(Debug: Detected emotion: {detected_emotion})")

        ere_engine.adjust_pathway_weights(detected_emotion)

        ai_response = ere_engine.generate_response(user_input, current_emotion=detected_emotion)

        # Determine the dominant emotion from ERE's current state for reaction mapping
        dominant_emotion_for_reaction = max(ere_engine.pathway_weights, key=ere_engine.pathway_weights.get)
        reaction_output = reaction_mapper.get_reaction(dominant_emotion_for_reaction)
        
        # Display the AI's response with the visual reaction (emoji)
        print(f"AI ({reaction_output['visual']}): {ai_response}")
        # print(f"(Debug: Suggested sound: {reaction_output['sound']}, Haptic: {reaction_output['haptic']})") # For future integrations


        if args.mode == "persistent":
            # For demonstration, storing a hash. In real system, this would be highly contextual/filtered.
            virem_vault.store_block(f"context_marker_{hash(user_input)}", f"Processed input for {detected_emotion}")

        consciousness_loop.pulse(ere_engine.pathway_weights, detected_emotion)


if __name__ == "__main__":
    main()
