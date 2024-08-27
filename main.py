import os
import logging
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from clicker import WebDriverInitializer, ClickerGenerator
from parser import NewsParser, Locator
from recorder import CrawledLinksLogger
from common import AccountManager, CrawledDataManager
from clustering_manager import GreedySlimeManager
from classification_manager import NeuroKumokoManager
from copyToaster_manager import CopyToasterManager

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main(target_url, filename, link_locator=None, limit=None, directory="data"):
    try:
        logger.info(f"Initializing WebDriver for URL: {target_url}")
        target_initializer = WebDriverInitializer(url=target_url)
        target_driver = target_initializer.initialize()

        # Initialize AccountManager
        account_manager = AccountManager(filename="config/account.info")

        # Initialize Locator
        locator = Locator()

        # Initialize CrawledLinksLogger instance
        crawled_links_logger = CrawledLinksLogger()

        if target_driver is None:
            logger.error(
                "Failed to initialize WebDriver for target URL. Exiting.")
            return None, None

        logger.info("WebDriver initialized successfully for target URL")

        # Create ClickerGenerator using the default locator
        clicker = ClickerGenerator(
            driver=target_driver, locator=link_locator)

        # Explicit wait for the presence of links
        # Wait up to 20 seconds (adjust as needed)
        wait = WebDriverWait(target_driver, 20)
        element_present = EC.presence_of_all_elements_located(
            (By.XPATH, clicker.locator))
        wait.until(element_present)

        # Generate links and filter uncrawled ones
        links = clicker.generate(limit=limit)
        logger.info(f"Found {len(links)} links to click")

        # Filter out already crawled links
        links = crawled_links_logger.find_new_uncrawled_links(links)

        # Parse webpage
        news_parser = NewsParser(driver=target_driver)
        results = []
        for link in links:
            try:
                if news_parser.get_page_with_retries(url=link):

                    result = news_parser.parse(
                        url=link, locator_key="default")
                    if result:
                        results.append(result)
                        crawled_links_logger.write_crawled_link(link)
            except Exception as e:
                logger.error(f"Failed to load {
                             link} after multiple attempts: {str(e)}")

        logger.info(f"Results collected for {filename}: {results}")
        full_path = news_parser.save_results_to_json(
            results, filename, directory=directory)

        # GreedySlime Manager
        greedySlime_manager = GreedySlimeManager(account_manager)
        greedySlime_manager.build_model(filename)

        source = greedySlime_manager.extract_and_transform_clusters()

        # CopyToaster Manager
        copyToater_manager = CopyToasterManager(account_manager)
        copyToater_manager.build_model(filename, source)       

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return None, None
    finally:
        if target_driver:
            target_driver.quit()

if __name__ == "__main__":
    #target_urls = [
        #"https://house.udn.com/house/index",
        #"https://udn.com/news/cate/2/7225"
    #]
    #filenames = ["house", "international_media"]

    #for target_url, filename in zip(target_urls, filenames):
        #main(target_url, filename, limit=5)
        
    # 测试用例
    response = {
        'status': True,
        'progress_status': 'completed',
        'msg': 'Success!',
        'result_list': [
            {
                'lexicon': 'cluster_1',
                'lexicon_score': 3.958603545179421,
                'llm': {
                    'usage': {
                        'prompt_tokens': 1133,
                        'completion_tokens': 81
                    },
                    'summary': '在巴黎舉行的奧運會雖然帶來了經濟商機，但卻也引發居民怨懟。政治角力在市長與總統之間展開，反映出這場盛事複雜的社會影響。',
                    'key_info': ['巴黎奧運', '居民怨懟', '政治角力', '經濟商機']
                }
            }
        ]
    }        
        
    lexicons = extract_lexicon_values(response)
    print(lexicons)  # 输出: ['cluster_1']        
