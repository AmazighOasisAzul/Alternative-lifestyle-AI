#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Terminal Interface
A personal AI for alternative diet, looksmaxxing, pharmacology, and blackpill knowledge
"""

import argparse
import sys
from generator import BlackpillGenerator
from retriever import DualModeRetriever


class BlackpillCLI:
    def __init__(self):
        self.generator = BlackpillGenerator()
        self.retriever = DualModeRetriever()
        try:
            self.retriever.load_vector_store()
        except Exception as e:
            print(f"Warning: Could not load vector store: {e}")
            print("Run 'python crawler.py' and 'python indexer.py' first")
    
    def query(self, query: str, mode: str = "fast", max_results: int = 5, use_last_resort: bool = True):
        if mode == "fast":
            context, mode, used_last_resort = self.retriever.retrieve_with_fallback(
                query, k=max_results, use_last_resort=use_last_resort
            )
        elif mode == "deep":
            context, mode = self.retriever.deep_retrieve(query, max_results=max_results)
            used_last_resort = False
        else:
            context, mode = self.retriever.youtube_retrieve(query, max_results=max_results)
            used_last_resort = False
        
        answer = self.generator.generate(
            query, context, mode, max_tokens=1024, use_last_resort=used_last_resort
        )
        
        if used_last_resort:
            answer = "\n⚠️  [LAST RESORT SOURCES USED - Incel forums referenced]\n" + answer
        
        return answer
    
    def interactive_mode(self):
        print("\n" + "="*60)
        print("  BLACKPILL LIFESTYLE AI - Terminal Interface")
        print("="*60)
        print("Core Philosophy: Bernard was right. The microbe is nothing,")
        print("                 the terrain is everything.")
        print("\nType 'quit', 'exit', or 'q' to end the session.")
        print("Type 'help' for commands.")
        print("\n" + "-"*60)
        
        current_mode = "fast"
        
        while True:
            try:
                query = input("\n[blackpill] > ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\nExiting Blackpill Lifestyle AI.")
                    break
                
                if query.lower() in ['help', '?']:
                    self.print_help()
                    continue
                
                if query.lower().startswith('mode '):
                    mode = query[5:].strip().lower()
                    if mode in ['fast', 'deep', 'youtube']:
                        current_mode = mode
                        print(f"Mode set to: {mode}")
                        continue
                    else:
                        print("Available modes: fast, deep, youtube")
                        continue
                
                answer = self.query(query, mode=current_mode)
                print(f"\n{answer}\n")
                
            except KeyboardInterrupt:
                print("\nUse 'quit' or 'exit' to end the session.")
            except EOFError:
                print("\nExiting Blackpill Lifestyle AI.")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def print_help(self):
        print("\n" + "-"*60)
        print("COMMANDS:")
        print("  help, ?          - Show this help message")
        print("  quit, exit, q    - Exit the terminal")
        print("  mode <name>      - Set mode (fast, deep, youtube)")
        print("\nQUERY EXAMPLES:")
        print("  What is terrain theory?")
        print("  How does mewing work?")
        print("  Best diet for mitochondrial health")
        print("  Looksmaxxing procedures for jaw")
        print("\nNOTES:")
        print("  - This is a PERSONAL AI for alternative lifestyle knowledge")
        print("  - Responses are blackpilled and biologically realistic")
        print("  - Last resort sources (incel forums) used only when necessary")
        print("  - Faustian approach: acknowledge struggle, emphasize improvement")
        print("-"*60)
    
    def one_shot(self, query: str, mode: str = "fast", no_last_resort: bool = False):
        use_last_resort = not no_last_resort
        answer = self.query(query, mode=mode, use_last_resort=use_last_resort)
        print(answer)


def main():
    parser = argparse.ArgumentParser(
        description="Alternative Lifestyle AI - Terminal Interface",
        epilog="Example: python cli.py -i"
    )
    parser.add_argument('query', nargs='?', help='Query to ask the AI')
    parser.add_argument('-i', '--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('-m', '--mode', choices=['fast', 'deep', 'youtube'], default='fast')
    parser.add_argument('--no-last-resort', action='store_true', help='Disable last resort sources')
    parser.add_argument('-v', '--version', action='version', version='Alternative Lifestyle AI v3.0.0')
    
    args = parser.parse_args()
    cli = BlackpillCLI()
    
    if args.interactive or not args.query:
        cli.interactive_mode()
    else:
        cli.one_shot(args.query, mode=args.mode, no_last_resort=args.no_last_resort)


if __name__ == "__main__":
    main()