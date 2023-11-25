import scrapy
import json
import os
import time
import pandas as pd

total_blog = []
order_list = []


class ProjectSpider(scrapy.Spider):
    name = "project"
    allowed_domains = ["rategain.com"]
    start_urls = ["https://rategain.com/blog/page/1/"]

    def parse(self, response):
        for i in range(1, 10):
            title = f".with-image:nth-child({str(i)}) h6 a"
            product_title = response.css(title).css("::text").extract()

            if not product_title:
                title = f".category-blog:nth-child({str(i)}) h6 a"
                product_title = response.css(title).css("::text").extract()
                date = f".category-blog:nth-child({str(i)}) .material-design-icon-history-clock-button+ span"
                product_date = response.css(date).css("::text").extract()
                like = f".category-blog:nth-child({str(i)}) .zilla-likes"
                product_like = response.css(like).css("::text").extract()

                if product_like:
                    product_real = product_like[1]
                else:
                    product_real = product_like

                data = {
                    "Product Title": product_title,
                    "Product Date": product_date,
                    "Product Like": product_real
                }
                if product_title and product_date and product_real:
                    total_blog.append(data)
                    order_list.append(len(order_list) + 1)
                    # time.sleep(2)

            else:
                title = f".with-image:nth-child({str(i)}) h6 a"
                product_title = response.css(title).css("::text").extract()
                date = f".with-image:nth-child({str(i)}) .material-design-icon-history-clock-button+ span"
                product_date = response.css(date).css("::text").extract()
                image = f".with-image:nth-child({str(i)}) .rocket-lazyload"
                product_image = response.css(image).css("::attr(data-bg)").extract()
                like = f".with-image:nth-child({str(i)}) .zilla-likes"
                product_like = response.css(like).css("::text").extract()
                if product_like:
                    product_real = product_like[1]
                else:
                    product_real = product_like

                data = {
                    "Product Title": product_title,
                    "Product Date": product_date,
                    "Product Image": product_image,
                    "Product Like": product_real
                }
                if product_title and product_date and product_real and product_image:
                    total_blog.append(data)
                    order_list.append(len(order_list) + 1)
                    # time.sleep(2)

        # Check for the next page
        next_page = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            # Save data after processing the last page
            self.save_data()

    def save_data(self):
        given_path = "C:\\Users\\samee\\Desktop\\SIH"
        given_path = os.path.join(given_path, "blog_data.xlsx")

        # Sort total_blog based on order_list to maintain order
        sorted_blog = [total_blog[i - 1] for i in order_list]

        # Convert to DataFrame
        df = pd.DataFrame(sorted_blog)

        # Save to Excel
        df.to_excel(given_path, index=False)
