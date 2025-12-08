# -*- coding: utf-8 -*-
"""
Example of using multiple visits (to avoid being detected as a bot)
This example shows how to visit a page multiple times without being
detected as a bot.
"""

from scraper import WebScraper

def example_basic():
    """Basic multiple visits example"""
    print("=" * 70)
    print("Example 1: Simple multiple visits")
    print("=" * 70)
    
    # Create a scraper
    scraper = WebScraper("https://httpbin.org/user-agent")
    
    # Visit the page 3 times with a delay between 2 and 5 seconds
    stats = scraper.visit_multiple_times(
        count=3,
        min_delay=2,
        max_delay=5,
        random_agent=True
    )
    
    print(f"\n📊 Result: {stats['success']} out of {stats['total']} visits were successful")


def example_advanced():
    """Advanced multiple visits example with data extraction"""
    print("\n\n" + "=" * 70)
    print("Example 2: Multiple visits with data extraction")
    print("=" * 70)
    
    # Create a scraper for a news site
    scraper = WebScraper("https://example.com")
    
    # Visit the page 5 times
    stats = scraper.visit_multiple_times(
        count=5,
        min_delay=3,
        max_delay=8,
        random_agent=True
    )
    
    # Extract data after the last visit
    if scraper.soup:
        print("\n📄 Page information:")
        print(f"Title: {scraper.get_title()}")
        print(f"Number of links: {len(scraper.get_links())}")
        print(f"Number of images: {len(scraper.get_images())}")
        
        # Display visit history
        print("\n📋 Visit history:")
        for i, visit in enumerate(scraper.visit_history, 1):
            time_str = visit['time'].strftime('%H:%M:%S')
            status = visit.get('status', 'unknown')
            print(f"  {i}. Time: {time_str} - Status: {status}")


def example_custom():
    """Custom multiple visits example with user-defined settings"""
    print("\n\n" + "=" * 70)
    print("Example 3: Custom multiple visits settings")
    print("=" * 70)
    
    # Get settings from the user
    url = input("\nPage URL (default: https://example.com): ").strip() or "https://example.com"
    
    try:
        count = int(input("Number of visits (default: 3): ").strip() or "3")
        min_delay = int(input("Minimum delay (seconds, default: 2): ").strip() or "2")
        max_delay = int(input("Maximum delay (seconds, default: 6): ").strip() or "6")
    except ValueError:
        print("⚠️  Invalid input! The default values will be used.")
        count, min_delay, max_delay = 3, 2, 6
    
    # Perform the visit
    scraper = WebScraper(url)
    stats = scraper.visit_multiple_times(
        count=count,
        min_delay=min_delay,
        max_delay=max_delay,
        random_agent=True
    )
    
    # Save the results
    if scraper.soup and stats['success'] > 0:
        save = input("\nSave HTML? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            scraper.save_html("multi_visit_result.html")
            print("✅ HTML file saved!")


def main():
    """Run all examples"""
    print("\n🕷️  Multiple visits examples (to avoid being detected as a bot)\n")
    
    # Selection menu
    print("Select an example:")
    print("1. Basic example")
    print("2. Advanced example")
    print("3. Custom example")
    print("4. Run all examples")
    
    choice = input("\nYour choice (1-4): ").strip()
    
    if choice == '1':
        example_basic()
    elif choice == '2':
        example_advanced()
    elif choice == '3':
        example_custom()
    elif choice == '4':
        example_basic()
        example_advanced()
    else:
        print("❌ Invalid choice!")
    
    print("\n" + "=" * 70)
    print("✅ All examples have been successfully run!")
    print("=" * 70)


if __name__ == "__main__":
    main()
