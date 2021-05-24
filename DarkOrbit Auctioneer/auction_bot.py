import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import random
import time
from datetime import datetime

import bot_settings


def to_int(value):
    if value == '-':
        return 0

    value = value.replace('.', '')
    return int(value)


class DarkOrbitSpider(scrapy.Spider):
    name = "AuctionBot"

    timeout = bot_settings.timeout
    waited = False
    maximum_spree = bot_settings.buying_spree
    current_transaction = 0

    buy_for_credits = bot_settings.buy_for_credits
    minimum_value = bot_settings.minimum_gain_per_item

    def parse_timeout(self, response, call, timeout):
        if timeout <= 0:
            timeout = self.timeout*60
        time.sleep(timeout+random.random()-1)
        self.waited = True
        return call(response)

    def action_wrapper(self, response, call):
        time.sleep(0.5+random.random()/2)
        return call(response)

    def start_requests(self):
        url = 'https://www.darkorbit.com/'
        yield scrapy.Request(url, self.action_wrapper, cb_kwargs=dict(call=self.parse_login))

    def parse_login(self, response):
        return scrapy.FormRequest.from_response(
            response=response,
            formname='bgcdw_login_form',
            formdata={'username': bot_settings.login, 'password': bot_settings.password},
            callback=self.action_wrapper,
            cb_kwargs=dict(call=self.go_to_auction)
        )

    def go_to_auction(self, response):
        url = '/indexInternal.es?action=internalAuction'
        return scrapy.Request(
            url=response.urljoin(url),
            callback=self.action_wrapper,
            cb_kwargs=dict(call=self.parse_auction))

    def parse_auction(self, response):
        money = to_int(response.xpath("//div[@id='header_credits']/text()").get().strip())
        self.log("Money: " + str(money))

        now = datetime.now()
        if int(now.strftime("%M")) < 35:
            minutes = 35 - int(now.strftime("%M")) - 1
        else:
            minutes = 95 - int(now.strftime("%M")) - 1
        seconds = 60 - int(now.strftime("%S"))
        self.log("Remaining time = " + str(minutes) + ":" + str(seconds))

        j = 0
        t_minutes = 0
        t_seconds = 13
        while (minutes-t_minutes)*60 + (seconds-t_seconds) > self.timeout*60 + 13:
            j += 1
            t_minutes += self.timeout
            t_seconds += 15
            if t_seconds > 60:
                t_minutes += 1
                t_seconds -= 60

        wait_time = (minutes-t_minutes)*60 + (seconds-t_seconds)
        self.log(str(j) + ", " + str(t_minutes) + ":" + str(t_seconds) + ", " + str(wait_time))

        if (not self.waited and wait_time >= 0) or self.current_transaction >= 4:
            self.current_transaction = 0
            return scrapy.Request(
                url=response.url,
                callback=self.parse_timeout,
                cb_kwargs=dict(call=self.parse_auction, timeout=wait_time)
            )

        value_list = []
        bet_list = []
        active_bet = bot_settings.active_bet

        item_keys = response.xpath("//td[@class='auction_item_name_col']/../@itemkey").getall()
        index = 0

        for item in response.xpath("//td[@class='auction_item_name_col']/..").getall():
            name = Selector(text=item).xpath("//td[@class='auction_item_name_col']/text()").get().strip()
            current_bet = to_int(Selector(text=item).xpath("//td[@class='auction_item_current']/text()").get().strip())
            your_bet = to_int(Selector(text=item).xpath("//td[@class='auction_item_you']/text()").get().strip())
            value = to_int(Selector(text=item).xpath("//td[@class='auction_item_instant']/text()").get().strip())*2.5
            loot_id = Selector(text=item).xpath("//input[@id='" + item_keys[index] + "_lootId']/@value").get()
            auction_type = 'hour'
            if item_keys[index][5] == 'd':
                auction_type = 'day'
            if item_keys[index][5] == 'w':
                auction_type = 'week'

            for i, bet in enumerate(active_bet):
                if bet[0] == name and (current_bet > your_bet or current_bet == 0) and \
                        current_bet <= bet[1] - 10000 and \
                        current_bet + 10000 <= money:
                    bet_list.append((name, current_bet, bet[1], item_keys[index], loot_id, auction_type))

            if (current_bet > your_bet or current_bet == 0) and \
                    value - current_bet >= 10000 + self.minimum_value and \
                    current_bet + 10000 <= money:
                value_list.append((name, current_bet, value, item_keys[index], loot_id, auction_type))

            index += 1

        bet_list = sorted(bet_list, key=lambda auction: auction[2] - auction[1])
        bet_list.reverse()
        self.log(bet_list)

        value_list = sorted(value_list, key=lambda auction: auction[2] - auction[1])
        value_list.reverse()
        self.log(value_list)

        item_list = bet_list + value_list
        if not self.buy_for_credits:
            item_list = bet_list

        seen = set()
        seen_add = seen.add
        item_list = [x for x in item_list if not (x in seen or seen_add(x))]
        item_list = [x for x in item_list if x[4] != '']

        self.log(item_list)

        if wait_time > 0:
            j += 1

        self.log(len(item_list))
        self.log(j * self.maximum_spree + self.maximum_spree - 1 - self.current_transaction)

        if len(item_list) == 0 or len(item_list) <= j*self.maximum_spree + 3-self.current_transaction:
            if j == 0:
                return scrapy.Request(
                    url=response.url,
                    callback=self.parse_timeout,
                    cb_kwargs=dict(call=self.parse_auction, timeout=3)
                )
            else:
                self.current_transaction = 0
                return scrapy.Request(
                    url=response.url,
                    callback=self.parse_timeout,
                    cb_kwargs=dict(call=self.parse_auction, timeout=wait_time)
                )

        item = item_list[j*self.maximum_spree + 3-self.current_transaction]

        self.log(item)
        self.current_transaction += 1
        self.log(self.current_transaction)

        return scrapy.FormRequest.from_response(
            response=response,
            formname='placeBid',
            formdata={'auctionType': item[5],
                      'subAction': 'bid',
                      'lootId': item[4],
                      'itemId': item[3],
                      'credits': str(item[1] + 10000)},
            callback=self.action_wrapper,
            cb_kwargs=dict(call=self.go_to_auction)
        )


process = CrawlerProcess(settings={
    'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
})

process.crawl(DarkOrbitSpider)
process.start()
