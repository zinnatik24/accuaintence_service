from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.youtube.com/shorts/r8DDw3eFVYA'

html = '''<div id="factoids" class="style-scope ytd-video-description-header-renderer"><factoid-renderer class="ytwFactoidRendererHost"><div class="ytwFactoidRendererFactoid" role="text" aria-label="28 тысяч отметок &quot;Нравится&quot;"><span class="ytwFactoidRendererValue"><span class="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap" role="text">28&nbsp;тыс.</span></span><span class="ytwFactoidRendererLabel"><span class="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap" role="text">Отметки "Нравится"</span></span></div></factoid-renderer><view-count-factoid-renderer><factoid-renderer class="ytwFactoidRendererHost"><div class="ytwFactoidRendererFactoid" role="text" aria-label="611&nbsp;829 просмотров"><span class="ytwFactoidRendererValue"><span class="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap" role="text">611&nbsp;829</span></span><span class="ytwFactoidRendererLabel"><span class="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap" role="text">Просмотры</span></span></div></factoid-renderer></view-count-factoid-renderer><factoid-renderer class="ytwFactoidRendererHost"><div class="ytwFactoidRendererFactoid" role="text" aria-label="9 окт. 2021 г."><span class="ytwFactoidRendererValue"><span class="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap" role="text">2021</span></span><span class="ytwFactoidRendererLabel"><span class="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap" role="text">9 окт.</span></span></div></factoid-renderer></div>
<div id="title" class="style-scope ytd-video-description-header-renderer">
  <yt-formatted-string class="style-scope ytd-video-description-header-renderer">How Much YouTube Shorts Paid Me For 30 Million Views</yt-formatted-string>
</div>
<h2 id="title" class="style-scope ytd-engagement-panel-title-header-renderer" aria-label="Комментарии 1,9&nbsp;тыс." tabindex="-1"> 
  <yt-formatted-string id="title-text" ellipsis-truncate="" class="style-scope ytd-engagement-panel-title-header-renderer" ellipsis-truncate-styling="" title="Комментарии">Комментарии</yt-formatted-string>
  <yt-formatted-string id="contextual-info" class="style-scope ytd-engagement-panel-title-header-renderer">1,9&nbsp;тыс.</yt-formatted-string>
</h2>
<span class="yt-core-attributed-string yt-avatar-stack-view-model-wiz__avatar-stack-text yt-core-attributed-string--white-space-pre-wrap yt-core-attributed-string--link-inherit-color" role="text"><span class="yt-core-attributed-string--link-inherit-color" style="color: rgb(170, 170, 170);">@jensentung</span></span>'''

soup = BeautifulSoup(html, 'html.parser')
res = {'URL': url}

title_tag = soup.select_one('#title yt-formatted-string')
res['Title'] = title_tag.text.strip() if title_tag else None

for i in soup.select('#factoids .ytwFactoidRendererFactoid'):
    label = i['aria-label']
    if 'Нравится' in label:
        v = label.split()[0]
        res['Like count'] = int(float(v.replace(',', '.')) * 1000) if 'тыс' in label else int(v.replace(' ', '').replace('\xa0', ''))
    elif 'просмотров' in label:
        res['Views'] = int(''.join(filter(str.isdigit, label)))
    elif 'г.' in label:
        res['Upload date'] = label

comments_tag = soup.select_one('h2#title yt-formatted-string#contextual-info')
if comments_tag:
    v = comments_tag.text.replace('\xa0', '').replace(',', '.').replace(' ', '')
    res['Comments'] = int(float(v.replace('тыс.', '')) * 1000) if 'тыс' in comments_tag.text else int(v)

channel_tag = soup.select_one('span.yt-avatar-stack-view-model-wiz__avatar-stack-text span')
res['Channel'] = channel_tag.text.strip() if channel_tag else None

cols_order = ['URL', 'Channel', 'Title', 'Like count', 'Views', 'Comments', 'Upload date']
df = pd.DataFrame([{k: res.get(k) for k in cols_order}])
df