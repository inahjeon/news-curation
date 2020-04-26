from datetime import datetime, timedelta

from tqdm import tqdm

from crawler.driver import get_chrome_driver


_SECTIONS = {
    '100': '정치',
    '101': '경제',
    '102': '사회',
    '103': '생활/문화',
    '104': '세계',
    '105': 'IT/과학'
}


def get_popular_day_news_contents(date, section_id):
    url = f'https://news.naver.com/main/ranking/popularDay.nhn' \
        f'?rankingType=popular_day' \
        f'&sectionId={section_id}&date={date}'
    driver.get(url)
    driver.implicitly_wait(1)

    ranking = driver.find_elements_by_class_name('ranking')

    if ranking:
        headlines = ranking[0].find_elements_by_class_name('ranking_headline')
        ledes = ranking[0].find_elements_by_class_name('ranking_lede')
        offices = ranking[0].find_elements_by_class_name('ranking_office')
        views = ranking[0].find_elements_by_class_name('ranking_view')

        return zip(headlines, ledes, offices, views)
    else:
        return None


def get_popular_day_news(driver, start_date, end_date):
    fp = open(f'./popularDay-{start_date}-{end_date}.tsv', 'w')
    columns = ['date', 'section', 'office', 'view', 'headline', 'lede', 'link']
    fp.write('\t'.join(columns) + '\n')

    target_dates = get_date_strings(start_date, end_date)

    for date_str in tqdm(target_dates):
        for section_id, section_name in _SECTIONS.items():
            contents = get_popular_day_news_contents(date_str, section_id)
            if contents:
                for headline, lede, office, view in contents:
                    headline_a_tag = headline.find_element_by_tag_name('a')
                    contents = '\t'.join([
                        date_str,
                        section_name,
                        office.text,
                        view.text,
                        headline_a_tag.get_attribute('title'),
                        lede.text,
                        headline_a_tag.get_attribute('href')
                    ])
                    fp.write(contents + '\n')

    driver.quit()


def get_date_strings(start_date, end_date):
    date_strings = []
    curr = datetime.strptime(start_date, '%Y%m%d')
    end = datetime.strptime(end_date, '%Y%m%d')

    while True:
        if curr > end:
            break
        else:
            date_strings.append(
                curr.strftime('%Y%m%d')
            )
            curr = curr + timedelta(days=1)
    return date_strings


if __name__ == '__main__':
    driver = get_chrome_driver()
    start_date = '20200101'
    end_date = '20200131'

    date_strings = get_date_strings(start_date, end_date)
    print(date_strings)
    get_popular_day_news(driver, start_date, end_date)
