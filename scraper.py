"""
Web Scraper with Anti-Bot Detection Features
This scraper is designed to visit and extract information from web pages with bot detection avoidance capabilities
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from typing import List, Dict, Optional


class WebScraper:
    """Scraper class with anti-bot detection capabilities"""
    
    # List of diverse User-Agents to simulate different browsers
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    ]
    
    def __init__(self, url: str):
        """
        Class constructor
        
        Args:
            url: Web page URL
        """
        self.url = url
        self.soup = None
        self.html_content = None
        self.response = None
        self.visit_history: List[Dict] = []
        
    def _get_random_headers(self) -> Dict[str, str]:
        """
        Create HTTP headers with random User-Agent
        
        Returns:
            Header dictionary
        """
        return {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    
    def _get_static_headers(self) -> Dict[str, str]:
        """
        Create HTTP headers with static User-Agent
        
        Returns:
            Header dictionary
        """
        return {
            'User-Agent': self.USER_AGENTS[0],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def visit_page(self, random_agent: bool = False) -> bool:
        """
        Visit a web page
        
        Args:
            random_agent: Use random User-Agent
            
        Returns:
            True on success, False on failure
        """
        try:
            # Select appropriate headers
            headers = self._get_random_headers() if random_agent else self._get_static_headers()
            
            # Send request
            print(f"🌐 Visiting: {self.url}")
            self.response = requests.get(
                self.url, 
                headers=headers, 
                timeout=10,
                allow_redirects=True
            )
            
            # Check response status
            self.response.raise_for_status()
            
            # Process HTML
            self.html_content = self.response.text
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
            
            # Record in history
            self.visit_history.append({
                'time': datetime.now(),
                'status': self.response.status_code,
                'success': True,
                'url': self.url
            })
            
            print(f"✅ Visit successful - Status code: {self.response.status_code}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Visit error: {e}")
            
            # Record error in history
            self.visit_history.append({
                'time': datetime.now(),
                'status': 'error',
                'success': False,
                'error': str(e),
                'url': self.url
            })
            
            return False
    
    def visit_multiple_times(
        self, 
        count: int = 3, 
        min_delay: int = 2, 
        max_delay: int = 5,
        random_agent: bool = True
    ) -> Dict[str, any]:
        """
        Multiple page visits with random delays (to avoid bot detection)
        
        Args:
            count: Number of visits
            min_delay: Minimum delay between visits (seconds)
            max_delay: Maximum delay between visits (seconds)
            random_agent: Use random User-Agent
            
        Returns:
            Dictionary containing visit statistics
        """
        print(f"\n{'='*70}")
        print(f"🕷️  Starting multiple visits: {count} times")
        print(f"⏱️  Delay: {min_delay}-{max_delay} seconds")
        print(f"🎭 Random User-Agent: {'Yes' if random_agent else 'No'}")
        print(f"{'='*70}\n")
        
        success_count = 0
        
        for i in range(count):
            print(f"📍 Visit {i + 1}/{count}")
            
            # Visit the page
            if self.visit_page(random_agent=random_agent):
                success_count += 1
            
            # Random delay between visits (except for the last visit)
            if i < count - 1:
                delay = random.uniform(min_delay, max_delay)
                print(f"⏳ Waiting {delay:.1f} seconds until next visit...\n")
                time.sleep(delay)
        
        # Calculate statistics
        stats = {
            'total': count,
            'success': success_count,
            'failed': count - success_count,
            'success_rate': (success_count / count) * 100 if count > 0 else 0
        }
        
        print(f"\n{'='*70}")
        print(f"📊 Final statistics:")
        print(f"   ✅ Successful: {stats['success']}")
        print(f"   ❌ Failed: {stats['failed']}")
        print(f"   📈 Success rate: {stats['success_rate']:.1f}%")
        print(f"{'='*70}\n")
        
        return stats
    
    def get_title(self) -> Optional[str]:
        """
        Extract page title
        
        Returns:
            Page title or None
        """
        if self.soup:
            title_tag = self.soup.find('title')
            return title_tag.get_text().strip() if title_tag else None
        return None
    
    def get_links(self) -> List[str]:
        """
        Extract all page links
        
        Returns:
            List of link URLs
        """
        if self.soup:
            links = []
            for link in self.soup.find_all('a', href=True):
                links.append(link['href'])
            return links
        return []
    
    def get_images(self) -> List[str]:
        """
        Extract all page images
        
        Returns:
            List of image URLs
        """
        if self.soup:
            images = []
            for img in self.soup.find_all('img', src=True):
                images.append(img['src'])
            return images
        return []
    
    def get_text(self) -> Optional[str]:
        """
        Extract page text
        
        Returns:
            Page text or None
        """
        if self.soup:
            return self.soup.get_text(separator='\n', strip=True)
        return None
    
    def save_html(self, filename: str = "output.html") -> bool:
        """
        Save HTML content to file
        
        Args:
            filename: Output filename
            
        Returns:
            True on success, False on failure
        """
        if self.html_content:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.html_content)
                print(f"✅ HTML file saved: {filename}")
                return True
            except Exception as e:
                print(f"❌ File save error: {e}")
                return False
        else:
            print("❌ HTML content not available!")
            return False
    
    def get_visit_history(self) -> List[Dict]:
        """
        Get visit history
        
        Returns:
            List of visit history
        """
        return self.visit_history
    
    def print_summary(self):
        """Print summary of extracted information"""
        if not self.soup:
            print("❌ You must visit the page first!")
            return
        
        print(f"\n{'='*70}")
        print("📄 Page Information Summary")
        print(f"{'='*70}")
        print(f"🔗 URL: {self.url}")
        print(f"📌 Title: {self.get_title()}")
        print(f"🔗 Number of links: {len(self.get_links())}")
        print(f"🖼️  Number of images: {len(self.get_images())}")
        print(f"📊 Number of visits: {len(self.visit_history)}")
        
        if self.visit_history:
            successful_visits = sum(1 for v in self.visit_history if v.get('success', False))
            print(f"✅ Successful visits: {successful_visits}/{len(self.visit_history)}")
        
        print(f"{'='*70}\n")


def main():
    """Main function for testing the scraper"""
    print("\n" + "="*70)
    print("🕷️  Python Web Scraper with Anti-Bot Features")
    print("="*70 + "\n")
    
    # Get URL from user
    url = input("🌐 Enter page URL (default: https://example.com): ").strip()
    if not url:
        url = "https://example.com"
    
    # Create scraper instance
    scraper = WebScraper(url)
    
    # Selection menu
    print("\nSelect visit type:")
    print("1. Simple visit (single time)")
    print("2. Multiple visits with random delay (anti-bot)")
    
    choice = input("\nYour choice (1 or 2): ").strip()
    
    if choice == '1':
        # Simple visit
        if scraper.visit_page(random_agent=True):
            scraper.print_summary()
            
            # Ask to save
            save = input("\n💾 Do you want to save the HTML? (y/n): ").strip().lower()
            if save in ['y', 'yes']:
                scraper.save_html()
    
    elif choice == '2':
        # Multiple visits
        try:
            count = int(input("\n📊 Number of visits (default: 3): ").strip() or "3")
            min_delay = int(input("⏱️  Minimum delay in seconds (default: 2): ").strip() or "2")
            max_delay = int(input("⏱️  Maximum delay in seconds (default: 5): ").strip() or "5")
        except ValueError:
            print("⚠️  Invalid input! Using default values.")
            count, min_delay, max_delay = 3, 2, 5
        
        # Start multiple visits
        stats = scraper.visit_multiple_times(
            count=count,
            min_delay=min_delay,
            max_delay=max_delay,
            random_agent=True
        )
        
        # Show summary
        if stats['success'] > 0:
            scraper.print_summary()
            
            # Ask to save
            save = input("\n💾 Do you want to save the HTML from the last visit? (y/n): ").strip().lower()
            if save in ['y', 'yes']:
                scraper.save_html("multi_visit_result.html")
    
    else:
        print("❌ Invalid choice!")
    
    print("\n" + "="*70)
    print("✅ Scraper executed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
