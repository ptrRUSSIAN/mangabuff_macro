from parser import MangaParser
from config import ParserConfig

def main():
    print("="*60)
    print("🦊 MangaBuff Parser")
    print("="*60)
    print("1 - Login only (save cookies)")
    print("2 - Full parsing")
    print("="*60)
    
    choice = input("Enter mode (1 or 2): ").strip()
    
    config = ParserConfig()
    parser = MangaParser(config, headless=False)
    
    try:
        if choice == "1":
            parser.login_only()
        elif choice == "2":
            parser.parse_manga()
        else:
            print("❌ Invalid choice")
    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted by user (Ctrl+C)")
    finally:
        parser.cleanup()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()