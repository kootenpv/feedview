__project__ = "feed_viewer"
__version__ = "0.0.0"
__repo__ = "https://github.com/kootenpv/feed_viewer"

import sys
import time
import tempfile
import webbrowser
import feedparser
from jinja2 import Template

template = Template("""
    <html><body>
    <h1>{{feed.channel.title}}</h1>
    {% for entry in feed.entries %}
      <h3><a href="{{entry.link}}">{{entry.title}}</a></h3>
      <div>
          Published at
          {% if entry.date %}
             {{entry.date}}
          {% elif entry.published %}
             {{entry.published}}
          {% elif entry.publication_date %}
             {{entry.publication_date}}
          {% else %}
             <unknown>
          {% endif %}
      </div>
      <p>{{entry.description}}</p>
      <button onclick="showCode({{loop.index}})">Show JSON</button>
      <p id="div{{loop.index}}" style="display: none">
         <code style="word-break: normal; word-wrap: normal; white-space: pre;">{{ entry | tojson(indent=4) }}</code>
      </p>
    {% endfor %}
    </body>
    <script>
function showCode(i) {
    var x = document.getElementById('div' + i);
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}
    </script></html
""")


def main():
    url = sys.argv[1]
    feed = feedparser.parse(url)

    html = template.render(feed=feed)
    with tempfile.NamedTemporaryFile(mode="w", suffix='.html', delete=False) as f:
        f.write(html)
        f.flush()
        webbrowser.open('file://' + f.name)
        time.sleep(1)


if __name__ == '__main__':
    main()
