# presence_ai/run_demo.py

import argparse
import os
import atexit
import shutil
import datetime # Added for generating unique block IDs in persistent mode

from config.config import Config
from ere_core.ere_engine import EREEngine
from virem_vault.auth_layer import AuthLayer
from virem_vault.driver import VIREMVaultDriver
from virem_vault.scratchpad import ScratchpadVault
from ere_core.loop_consciousness import LoopConsciousness
from ere_core.reaction_mapper import ReactionMapper
from virem_vault.vault_block_filter import VaultBlockFilter

# --- Conceptual Session Lifetime & RAM Teardown ---
# This path simulates a temporary RAM-only storage area that is cleaned on exit.
# In a true RAM-only scenario, data wouldn't even touch the filesystem.
RAM_SCRATCH_PATH = "scratch_memory"

def initialize_ram_scratch():
    """Initializes the conceptual RAM scratch directory."""
    os.makedirs(RAM_SCRATCH_PATH, exist_ok=True)
    print(f"RAM scratch directory initialized at: {RAM_SCRATCH_PATH}")

def teardown_ram_scratch():
    """Tears down (deletes) the conceptual RAM scratch directory."""
    if os.path.exists(RAM_SCRATCH_PATH):
        shutil.rmtree(RAM_SCRATCH_PATH, ignore_errors=True)
        print(f"RAM scratch directory '{RAM_SCRATCH_PATH}' torn down.")

# Register the teardown function to run automatically when the script exits
atexit.register(teardown_ram_scratch)
# --- End of Conceptual Teardown ---


def main():
    # Load configuration settings (from config/config.json)
    app_config = Config()

    parser = argparse.ArgumentParser(description="Run Stateless AI with Affective Soft Memory.")
    parser.add_argument(
        "--mode",
        type=str,
        default=app_config.DEFAULT_MODE, # Default mode loaded from config.json
        choices=["scratch", "persistent"],
        help=f"Operating mode: 'scratch' (RAM-only, zero-trace) or 'persistent' (ChaCha20 encrypted file-based, privacy-preserving). Default: {app_config.DEFAULT_MODE}"
    )
    args = parser.parse_args()

    print(f"--- Starting Stateless AI Demo in {args.mode.upper()} Mode ---")

    # If in 'scratch' mode, initialize the conceptual RAM scratchpad
    if args.mode == "scratch":
        initialize_ram_scratch()

    # 1. Authentication Layer
    auth_layer = AuthLayer()
    if not auth_layer.authenticate(mode=args.mode):
        print("Authentication failed. Exiting.")
        return

    # 2. VIREM Vault Initialization
    if args.mode == "scratch":
        virem_vault = ScratchpadVault()
        print("VIREM Vault: Operating in RAM-only Scratchpad mode.")
    else: # persistent mode
        # The vault_path is now derived from config.json -> config.py
        virem_vault = VIREMVaultDriver(vault_path=app_config.VAULT_PATH)
        print(f"VIREM Vault: Operating in persistent encrypted mode. Vault path: {app_config.VAULT_PATH}.")

    # 3. Emotive Resonance Engine (ERE) Initialization
    ere_engine = EREEngine()
    print("ERE Engine: Initialized for affective resonance and behavioral adaptation.")

    # 4. Loop Consciousness Initialization
    # Simulates the AI's internal heartbeat, introspection, and temporal memory
    consciousness_loop = LoopConsciousness(heartbeat_interval=3.0, memory_capacity=5)
    print("Consciousness loop initialized for internal self-awareness.")

    # 5. Reaction Mapper Initialization
    # Maps internal emotional states to external expressions (e.g., emojis)
    reaction_mapper = ReactionMapper()
    print("Reaction mapper initialized for emotional expression.")

    # 6. Vault Block Filter Initialization
    # Controls which emotionally significant blocks get persisted in 'persistent' mode
    vault_block_filter = VaultBlockFilter()
    print("Vault block filter initialized for selective memory storage based on emotional significance.")


    # --- Main Interaction Loop ---
    print("\nAI is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("\nExiting session. Ensuring all ephemeral memory is cleared.")
            if args.mode == "persistent":
                virem_vault.clear_vault() # Clear persistent encrypted vault file
            elif args.mode == "scratch":
                virem_vault.clear_session_memory() # Clear RAM scratchpad data explicitly
            break # Exit the loop

        # 1. Detect emotion from user input (using ere_core/emotion_parser.py internally)
        detected_emotion = ere_engine.detect_emotion(user_input)
        print(f"(Debug: Detected emotion: {detected_emotion})")

        # 2. Adjust ERE pathway weights based on detected emotion (soft memory learning)
        ere_engine.adjust_pathway_weights(detected_emotion)

        # 3. Generate AI response based on current ERE state and soft memory biases
        ai_response = ere_engine.generate_response(user_input, current_emotion=detected_emotion)

        # 4. Get and display external reaction based on the AI's dominant emotional state
        dominant_emotion_for_reaction = max(ere_engine.pathway_weights, key=ere_engine.pathway_weights.get)
        reaction_output = reaction_mapper.get_reaction(dominant_emotion_for_reaction)
        
        print(f"AI ({reaction_output['visual']}): {ai_response}") # Display AI response with visual emoji/reaction

        # 5. Conditional Memory Persistence (only in 'persistent' mode)
        if args.mode == "persistent":
            # Check if the current emotional state meets conditions for a "significant" memory
            if vault_block_filter.should_store_block(ere_engine.pathway_weights):
                # Generate a unique, non-user-identifiable block ID for the significant moment
                block_id = f"emotional_peak_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
                
                # Store a highly encrypted, transient block representing the significant state.
                # This block does NOT contain user data, but metadata about the AI's internal experience.
                virem_vault.store_block(block_id, f"Significant emotional state detected: {dominant_emotion_for_reaction}, Current Weights: {ere_engine.pathway_weights}")
            else:
                print("(Debug: Block not stored in vault as emotional thresholds were not met for persistence.)")

        # 6. Pulse the consciousness loop for internal awareness and introspection
        consciousness_loop.pulse(ere_engine.pathway_weights, detected_emotion)


if __name__ == "__main__":
    main()
