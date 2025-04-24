import requests
from bs4 import BeautifulSoup
import pandas as pd

# 读取 Excel 表格
def read_excel(file_path):
    return pd.read_excel(file_path)

# 爬取学者的论文
def fetch_papers(person_name, lab_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(lab_url, headers=headers)
    
    if response.status_code != 200:
        print(f"无法访问网站: {lab_url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 假设每篇论文在网页上有 <a> 标签，并且有 "paper" 类名
    papers = []
    for a_tag in soup.find_all('a', class_='paper'):
        paper_title = a_tag.get_text()
        paper_link = a_tag.get('href')
        papers.append((paper_title, paper_link))
    
    return papers

# 将爬取的数据写入 HTML 文件
def save_to_html(data, output_file):
    html_content = "<html><head><title>Scholar Papers</title></head><body>"
    html_content += "<h1>Scholar Papers</h1>"
    html_content += "<table border='1'><tr><th>Name</th><th>Lab URL</th><th>Paper Title</th><th>Paper Link</th></tr>"
    
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td><a href='{row[3]}'>Link</a></td></tr>"
    
    html_content += "</table></body></html>"
    
    with open(output_file, 'w') as f:
        f.write(html_content)

# 主函数
def main(input_excel, output_html):
    # 读取输入的 Excel 文件
    data = read_excel(input_excel)
    
    # 用于存储爬取的数据
    results = []

    # 遍历每一行，爬取论文
    for index, row in data.iterrows():
        person_name = row['Name']
        lab_url = row['Lab URL']
        papers = fetch_papers(person_name, lab_url)
        
        for paper_title, paper_link in papers:
            results.append([person_name, lab_url, paper_title, paper_link])

    # 保存爬取的数据到 HTML 文件
    save_to_html(results, output_html)
    print(f"爬取的数据已保存到 {output_html}")

# 调用主函数
if __name__ == '__main__':
    input_excel = 'input_data.xlsx'  # 输入的 Excel 文件
    output_html = 'index.html'  # 输出的 HTML 文件
    main(input_excel, output_html)
