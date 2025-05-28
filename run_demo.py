import argparse
from config.config import Config
from ere_core.ere_engine import EREEngine
from virem_vault.auth_layer import AuthLayer
from virem_vault.driver import VIREMVaultDriver
from virem_vault.scratchpad import ScratchpadVault

def main():
    parser = argparse.ArgumentParser(description="Run Stateless AI with Affective Soft Memory.")
    parser.add_argument("--mode", type=str, default="scratch", choices=["scratch", "persistent"],
                        help="Operating mode: 'scratch' (RAM-only) or 'persistent' (ChaCha20 encrypted file-based).")
    args = parser.parse_args()

    # Load configuration
    app_config = Config()

    print(f"--- Starting Stateless AI Demo in {args.mode.upper()} Mode ---")

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
        virem_vault = VIREMVaultDriver(vault_path=app_config.VAULT_PATH)
        print(f"VIREM Vault: Using persistent encrypted vault at {app_config.VAULT_PATH}.")

    # 3. Emotive Resonance Engine Initialization
    # ERE Engine uses the vault for ephemeral "context" but doesn't store user data
    ere_engine = EREEngine()
    print("ERE Engine: Initialized for affective resonance.")

    # Main interaction loop (simplified)
    print("\nAI is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting session. All ephemeral memory cleared.")
            # In a real scenario, this would ensure scratchpad is truly cleared.
            break

        # Simulate processing:
        # 1. Detect emotion from user_input (ERE's job, simplified here)
        detected_emotion = ere_engine.detect_emotion(user_input)
        print(f"(Debug: Detected emotion: {detected_emotion})")

        # 2. Adjust ERE pathway weights based on detected emotion
        ere_engine.adjust_pathway_weights(detected_emotion)

        # 3. Generate response based on current ERE state and soft memory biases
        ai_response = ere_engine.generate_response(user_input, current_emotion=detected_emotion)
        print(f"AI: {ai_response}")

        # In persistent mode, the vault driver might periodically sync blocks (if designed that way)
        # In scratch mode, no data leaves RAM
        if args.mode == "persistent":
            # Example: Simulate ephemeral memory interaction via vault
            # This is NOT storing user data, but perhaps ephemeral "session context"
            # that's then immediately encrypted and decayed or overwritten.
            virem_vault.store_block(f"context_marker_{len(user_input)}", f"Processed input for {detected_emotion}")
            # Realistically, this would be highly transient and encrypted, never user data.


if __name__ == "__main__":
    main()
