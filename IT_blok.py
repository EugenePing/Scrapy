# -*- coding: utf-8 -*-
import json
import scrapy
import io


class ItBlokSpider(scrapy.Spider):
    name = 'IT-blok'
    start_urls = ['https://it-blok.com.ua/computeri.html']

    def parse(self, response):
        links = response.css('.item-title a::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, self.parse_pc)
        page = 0
        while page < 21:
            page += 1
            yield scrapy.Request('https://it-blok.com.ua/computeri.html?page=' + str(page), callback=self.parse)

    def parse_pc(self, response):
        pc_title = response.css('h1::text').get()
        pc_price = response.css('.special-price .price::text').get()
        pc_img = response.css('.thumbnails img::attr(src)').getall()
        pc_imgs = []
        for i in pc_img:
            pc_imgs.append('https://it-blok.com.ua/' + i)
        cpu_name = response.css('.attr-block:nth-child(1) tr:nth-child(1) td+ td::text').get()
        cpu_manufacturer = response.css('.attr-block:nth-child(1) tr:nth-child(4) td+ td::text').get()
        cpu_kernels = response.css('.attr-block:nth-child(1) tr:nth-child(5) td+ td::text').get()
        cpu_core_clock = response.css('.attr-block:nth-child(1) tr:nth-child(6) td+ td::text').get()
        power_supply = response.css('.attr-block:nth-child(6) tr:nth-child(1) td+ td::text').get()
        motherboard = response.css('.attr-block:nth-child(2) tr:nth-child(1) td+ td::text').get()
        ram = response.css('.attr-block:nth-child(3) tr:nth-child(1) td+ td::text').get()
        gpu_name = response.css('.attr-block:nth-child(4) tr:nth-child(2) td+ td::text').get()
        gpu_memory = response.css('.attr-block:nth-child(4) tr:nth-child(3) td+ td::text').get()
        memory = response.css('.attr-block:nth-child(5) td+ td::text').getall()
        if len(memory) > 1:
            memory1 = list()
            memory1.append('HDD:' + memory[0])
            memory1.append('SSD:' + memory[1])
            memory = memory1
        pc_body = response.css('.attr-block:nth-child(7) td+ td::text').get()

        dt = {
            'Имя ПК': pc_title,
            'Цена ПК': pc_price,
            'Фото ПК': pc_imgs,
            'Процессор': cpu_name,
            'Производитель процессора': cpu_manufacturer,
            'Количество ядер процессора': cpu_kernels,
            'Тактовая частота ядра': cpu_core_clock,
            'Мощность блока питания': power_supply,
            'Материнка': motherboard,
            'Оперативка': ram,
            'Видеокарта': gpu_name,
            'Видеопамять': gpu_memory,
            'Память': memory,
            'Корпус': pc_body,
        }

        yield dt

        # next_page = 'https://it-blok.com.ua/computeri.html?page=' + str

        f = open("IT-blok.json", "a", encoding='utf-8')
        json.dump(dt, f, ensure_ascii=False)
        f.close()
