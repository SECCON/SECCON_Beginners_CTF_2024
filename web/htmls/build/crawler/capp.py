import os
import uuid
import asyncio
from playwright.async_api import async_playwright
from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index_get():
    return render_template("index.html")


async def crawl(filename):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(java_script_enabled=False)
        page = await context.new_page()
        await page.goto(f"file:///var/www/htmls/{filename}", timeout=5000)
        await browser.close()


@app.route("/", methods=["POST"])
def index_post():
    try:
        html = request.form.get("html")
        filename = f"{uuid.uuid4()}.html"
        with open(f"htmls/{filename}", "w+") as f:
            f.write(html)
        asyncio.run(crawl(f"{filename}"))
        os.remove(f"htmls/{filename}")
    except:
        pass
    return render_template("ok.html")


@app.route("/flag/<path:flag_path>")
def flag(flag_path):
    return send_from_directory("htmls/ctf/", os.path.join(flag_path, "flag.txt"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=31417)
