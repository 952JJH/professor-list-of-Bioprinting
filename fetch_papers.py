import json
import feedparser
from datetime import datetime
from scholarly import scholarly

def get_2024_papers(google_scholar_id):
    # 通过Google Scholar获取论文
    author = scholarly.search_author_id(google_scholar_id)
    scholarly.fill(author, sections=['publications'])
    
    current_year = datetime.now().year
    papers = []
    for pub in author['publications']:
        if pub['bib'].get('pub_year', '') == str(current_year):
            papers.append({
                "title": pub['bib']['title'],
                "url": pub.get('pub_url', f"https://scholar.google.com/citations?user={google_scholar_id}#d=gs_md_cita-d&u=%2F{pub['author_pub_id']}")
            })
    return papers

# 加载学者列表
with open('scholars.json', 'r') as f:
    scholars = json.load(f)

# 生成Markdown内容
md_content = "# 🎓 学者最新论文（2024）\n\n"
for scholar in scholars:
    papers = get_2024_papers(scholar["google_scholar_id"])
    md_content += f"### [{scholar['name']}]({scholar['homepage']})\n"
    if papers:
        for paper in papers:
            md_content += f"- [{paper['title']}]({paper['url']})\n"
    else:
        md_content += "- 本年度暂无新论文\n"
    md_content += "\n"

# 更新README.md
with open('README.md', 'w') as f:
    f.write(md_content)
