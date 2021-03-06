#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script scrapes all the professors from the univaq website."""

import sys
sys.path.insert(0, '../')
from libs.utils import utils

PROFESSORS_URL = ("http://www.disim.univaq.it/didattica/"
                  "content.php?tipo=3&ordine=1&chiave=0&pid=25&did=8&lid=it&"
                  "frmRicercaNome=&frmRicercaCognome=&frmRicercaLaurea=1&action_search=Filtra")

def courses_cleanup(course):
    """Clean the courses' output"""
    return ', '.join([x for x in course.splitlines() if x and x[0] != u'\xa0'])

def email_soup_cleanup(email_soup):
    """Clean the emails' output"""
    if not email_soup.a:
        return ''
    email_soup.find('img', alt='at').replace_with('@')
    for img in email_soup.find_all('img'):
        img.replace_with('.')
    return email_soup.text.strip()  # .lower()  # ?

def phone_cleanup(s):
    """Clean the phones' output"""
    if not s:
        return ''
    s = ''.join([c for c in s if c.isdigit() or c == '+'])
    if s and s[0] != '+' and len(s) == 10:
        s = '+39' + s  # if not already internationalized, make it Italian
    return '-'.join([s[:3], s[3:7], s[7:]]) if s.startswith('+39') else s

def scrape_professors(url=PROFESSORS_URL):
    """Get information about professors"""

    scraped_professors = []
    soup = utils.get_soup_from_url(url)
    professor_names = soup.find("table").find_all(colspan='2')
    for name_cell in professor_names:
        name, phone, email, courses, _ = name_cell.parent.find_all('td')
        scraped_professors.append({
            "nome": name.text or "non disponibile",
            "telefono": phone_cleanup(phone.text) or "non disponibile",
            "e-mail": email_soup_cleanup(email) or "non disponibile",
            "corsi": courses_cleanup(courses.text) or "non disponibile",
        })
    return scraped_professors

if __name__ == "__main__":
    utils.write_json(scrape_professors(), "../json/professors.json")
