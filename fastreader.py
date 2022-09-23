#!/usr/bin/env python3

import argparse
import os
from time import sleep

from sys import argv

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


BACKGROUND_COLOR = (37, 150, 190)
FONT_COLOR = (255, 255, 255)
WORD_PER_MIN = 300
ALERT = ''


def render(screen, words):
    global WORD_PER_MIN
    paused = False
    i = 0
    while i < len(words):
        if words[i] == '':
            i += 1
            continue
        percentage = i / len(words)
        
        _, word_index = handle_event(screen, percentage, paused, words, i)

        if word_index != i:
            i = word_index
            continue


        render_all(screen, percentage, paused, words, i)
        word_interval = 60 / WORD_PER_MIN
        sleep(word_interval)
        i += 1
        
    return True


def handle_event(screen, percentage, paused, words, word_index):
    global WORD_PER_MIN
    global ALERT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise KeyboardInterrupt()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise KeyboardInterrupt()

            if event.key == pygame.K_SPACE:
                paused = not paused
                ALERT = ''
                while paused:
                    render_all(screen, percentage, paused, words, word_index)
                    paused, word_index = handle_event(screen, percentage, paused, words, word_index)
                    print('Word index: {}'.format(word_index))
                return False, word_index
            elif event.key == pygame.K_UP:
                WORD_PER_MIN += 10
            elif event.key == pygame.K_DOWN:
                WORD_PER_MIN -= 10
                if WORD_PER_MIN < 0:
                    WORD_PER_MIN = 0
            elif event.key == pygame.K_RIGHT:
                if paused:
                    word_index += 1
                    if word_index >= len(words):
                        word_index = len(words) - 1
                    render_all(screen, percentage, paused, words, word_index)
                else:
                    ALERT = 'You have to pause before changing words'
            elif event.key == pygame.K_LEFT:
                if paused:
                    word_index -= 1
                    if word_index < 0:
                        word_index = 0
                    render_all(screen, percentage, paused, words, word_index)
                else:
                    ALERT = 'You have to pause before changing words'
    print('Word index: {}'.format(word_index))
    return True, word_index


def load_words(file_name):
    with open(file_name, 'r') as f:
        return ' '.join(f.read().split('\n')).split(' ')


def render_all(screen, percentage, paused, words, word_index):
    screen.fill(BACKGROUND_COLOR)
    render_status(screen, percentage, paused)
    render_text(screen, words[word_index])
    render_alert(screen)
    pygame.display.flip()


def render_alert(screen):
    global ALERT
    if ALERT:
        font = pygame.font.SysFont('Arial', 30)
        text = font.render(ALERT, True, FONT_COLOR)
        screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, screen.get_height() - text.get_height()))
        pygame.display.flip()


def render_status(screen, percentage, paused):
    global WORD_PER_MIN
    print('Rendering status for {} words per minute, {}% done, paused: {}'.format(WORD_PER_MIN, percentage, paused))
    # print words per min on top left
    font = pygame.font.SysFont('Arial', 30)
    text = font.render('Words per minute: {}'.format(WORD_PER_MIN), True, FONT_COLOR)
    screen.blit(text, (0, 0))

    # print percentage on top right
    font = pygame.font.SysFont('Arial', 30)
    text = font.render('{:.2f}%'.format(percentage * 100), True, FONT_COLOR)
    screen.blit(text, (screen.get_width() - text.get_width(), 0))

    # print pause on top center
    if paused:
        font = pygame.font.SysFont('Arial', 30)
        text = font.render('Paused', True, FONT_COLOR)
        screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 0))


def render_text(screen, text):
    display_width, display_height = screen.get_size()
    text_width, text_height = pygame.font.Font(None, 100).size(text)
    screen.blit(pygame.font.SysFont("Arial", 100).render(text, True, FONT_COLOR), ((display_width - text_width) / 2, (display_height - text_height) / 2))


def cli_init():
    parser = argparse.ArgumentParser('fastreader')
    parser.add_argument('file_name', metavar='FILE', type=str, nargs='?', default='words.txt', help='file containing the text (default: words.txt)')
    args = parser.parse_args(argv[1:])
    return args


def validate_file(file_name):
    if not os.path.isfile(file_name):
        print('File not found: {}'.format(file_name))
        return False
    return True


def main():
    args = cli_init()
    file_name = args.file_name
    if not validate_file(file_name):
        return
    print('File:', file_name)
    words = load_words(file_name)

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Hello World")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not render(screen, words):
            running = False
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
