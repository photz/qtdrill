#!/usr/bin/env python3

import argparse, logging, sqlite3, random, os

from labelled_audiofile import LabelledAudiofile

logging.basicConfig(level=logging.INFO)



def importer():
    pass


def get_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('language',
                            choices=['kr', 'en', 'zh'])

    arg_parser.add_argument('user',
                            type=str,
                            help='name of the user who will be the owner')


    arg_parser.add_argument('sqlite3',
                            type=str)

    arg_parser.add_argument('target_dir',
                            type=str,
                            help='the directory in which the '
                            'the audio files will be stored')

    arg_parser.add_argument('audiofiles',
                            type=str,
                            help='audio files',
                            nargs='+')

    arg_parser.add_argument('--prefix',
                            type=str)

    arg_parser.add_argument('--output-format',
                            choices=['flac', 'ogg', 'mp3', 'wav'],
                            default='ogg')


    
    args = arg_parser.parse_args()

    return args


def insert_drill_section(db, language, name, description, user):
    cursor = db.cursor()

    q = '''
    INSERT INTO drill_sections
    (language_id, name, description, user_id, created_at, updated_at)
    VALUES ((SELECT id FROM languages WHERE code = ?),
            ?,
            ?,
            (SELECT id FROM users WHERE name = ?),
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP)
    '''

    cursor.execute(q, (language, name, description, user))

    return cursor.lastrowid

def insert_drill(db, drill_section_id, teacher, teacher_audio,
                 student, student_audio):
    cursor = db.cursor()

    q = '''
    INSERT INTO drills
    (drill_section_id, teacher, teacher_audio, student, student_audio, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    '''

    cursor.execute(q, (drill_section_id, teacher, teacher_audio,
                   student, student_audio))

    return cursor.lastrowid
            
def random_string():
    return ''.join(random.choice(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '0123456789') for _ in range(32))

def main():


    args = get_args()

    db = sqlite3.connect(args.sqlite3,
                         detect_types=sqlite3.PARSE_DECLTYPES)


    # tell sqlite to enforce foreign key constraints
    db.execute("PRAGMA foreign_keys = on;")


    for audiofile in args.audiofiles:

        labelled_audiofile = LabelledAudiofile(audiofile)
        labelled_audiofile.parse()

        for drill_section in labelled_audiofile.get_drill_sections():

            drill_section_id = insert_drill_section(db,
                                                    args.language,
                                                    drill_section.get_name(),
                                                    '',
                                                    args.user)

            logging.info('created new drill section with id {}'.format(drill_section_id))

            for drill in drill_section.get_drills():

                #print(drill.get_teacher().get_text(), 
                #drill.get_student().get_text())

                teacher_audio_name = random_string()
                student_audio_name = random_string()

                teacher_audio_path = os.path.join(args.target_dir,
                                                  teacher_audio_name + '.OGG')

                student_audio_path = os.path.join(args.target_dir,
                                                  student_audio_name + '.OGG')            

                logging.info('exporting teacher audio file to {}'.format(teacher_audio_path))

                logging.info('exporting student audio file to {}'.format(student_audio_path))

                drill.get_teacher().export(teacher_audio_path)

                drill.get_student().export(student_audio_path)

                insert_drill(db, drill_section_id,
                             drill.get_teacher().get_text(),
                             teacher_audio_name,
                             drill.get_student().get_text(),
                             student_audio_name)

            db.commit()

            break

if '__main__' == __name__:
    main()
