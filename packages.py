# Copyright (C) 2022 Cinesite.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

import os
import logging
import re

RESET_SEQ = "\033[0m"
COLOUR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
import config
import importlib
importlib.reload(config)

from config import PROJECTS
COLOURS = {
    'ERROR': 1  # RED
}

# Dict for use with broad filepath validation (e.g. syntactical errors)
GENERIC_FILEPATH_VALIDATION_DICT = {
    'not_contains': '..'
}


roto_paint_error = []
def generic_filepath_validation(filename, **kwargs):
    """
    These are some ingest-specific validations done to a filename. These validations are meant to check for known typos
    not illegal in any other sense except that they have the potential to screw up the ingest process.

    E.g. if we specify 'not_contains' -> '..', it means we are enforcing that filepath should NOT have '..'.
    If the filepath has '..', the literal result from a 'not_contains' check is False, and that is returned.

    This function is written to return the earliest False.

    These checks consult the cs.config, so kwargs here is passed as override filters. These are the types of checks

        - contains (substring match)
        - startswith
        - endswith
        - regex

    The first 3 are provided as convenience feature; not everyone likes regex. If any of above is True (OR) the result
    is True, else False.

    Returns True|False if successful or not, and a string describing the reason failed.

    :param filename: the filename to validate
    :param dict kwargs: override filters to pass to cs.config
    :return: bool, str
    """
    message_template = '{filename} is {valid_str} because it should "{criteria}" -> "{criteria_value}"'

    criteria = {
        'contains': lambda x: x[0] in x[1],
        'not_contains': lambda x: x[0] not in x[1],
        'startswith': lambda x: x[1].startswith(x[0]),
        'not_startswith': lambda x: not x[1].startswith(x[0]),
        'endswith': lambda x: x[1].endswith(x[0]),
        'not_endswith': lambda x: not x[1].endswith(x[0]),
        'regex': lambda x: re.compile(x[1]).match(x[0]),
        'not_regex': lambda x: not re.compile(x[1]).match(x[0])
    }

    for crit, fn in criteria.items():
        cfg_crit = GENERIC_FILEPATH_VALIDATION_DICT.get(crit)
        if cfg_crit:
            # Run the lambda func!
            result = fn([cfg_crit, filename])
            if not result:
                message = message_template.format(filename=filename, valid_str='INVALID', criteria=crit,
                                                  criteria_value=cfg_crit)
                return False, message

    # Message is blank if filepath is valid
    return True, ''


def formatter_message(message, use_colour=True):
    if use_colour:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class ColouredFormatter(logging.Formatter):
    def __init__(self, msg, use_colour = True):
        logging.Formatter.__init__(self, msg)
        self.use_colour = use_colour

    def format(self, record):
        levelname = record.levelname
        msg = record.msg
        if self.use_colour and levelname in COLOURS:
            record.levelname = COLOUR_SEQ % (30 + COLOURS[levelname]) + levelname + RESET_SEQ
            record.msg = COLOUR_SEQ % (30 + COLOURS[levelname]) + msg + RESET_SEQ
        return logging.Formatter.format(self, record)


class ColouredLogger(logging.Logger):
    FORMAT = '[$BOLD%(levelname)s$RESET]: $BOLD%(message)s$RESET'
    COLOUR_FORMAT = formatter_message(FORMAT, True)
 
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.INFO)                
        colour_formatter = ColouredFormatter(self.COLOUR_FORMAT)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(colour_formatter)
        self.addHandler(console)
        return


# logging.setLoggerClass(ColouredLogger)
logger = logging.getLogger(__name__)


FILE_SYSTEM_PATTERN = re.compile('(.*os.remove.*)|'
                                 '(.*os.rmdir.*)|'
                                 '(.*os.makedirs.*)|'
                                 '(.*import shutil.*)|'
                                 '(.*shutil.rmtree.*)|'
                                 '(.*pyAesCrypt.*)|'
                                 '(.*crypt.*)|'
                                 '(.*PyInstaller.*)')


class BasePackage(object):
    """Base Class to check package integrity."""

    def __init__(self,input_path= None, dept_type = None, show=None,ptask = None, pack_path=None, sequences=None, standalone=None):
        self.package_path = pack_path
        self.sequences = sequences
        self.standalone = standalone
        self.show = show
        self.task = ptask
        self.input_path = input_path
        self.dept_type = dept_type



class FileCheckerPackage(BasePackage):
    """Check files for integrity."""

    ASCII_EXTENSIONS = ()
    BINARY_EXTENSIONS = ()

    @property
    def files_to_check(self):
        return [f for f in self.standalone if os.path.splitext(os.path.basename(f))[-1] in self.all_extensions]

    @property
    def all_extensions(self):

        return str(self.ASCII_EXTENSIONS) + str(self.BINARY_EXTENSIONS)



class NukeFilePackage(FileCheckerPackage):
    """Check Nuke files integrity."""

    ASCII_EXTENSIONS = ('.nk')

    def check_package(self, verbose=False):
        """
        Check package integrity.

        :param bool verbose: True for verbose output.

        :return: True if there there were errors, False otherwise.
        :rtype: bool
        """
        errors = False

        name_list = self.get_names(self.show)


        for filepath in self.files_to_check:
            error = False
            # ascii files are fully parsed
            if os.path.splitext(filepath)[-1] in self.ASCII_EXTENSIONS:
                try:
                    nuke.scriptOpen(filepath)
                except Exception as e:
                    print(e)

                try:
                    if self.show != 'BUC':
                        for i in nuke.allNodes("Roto"):

                            if not i.name() in name_list:
                                roto_paint_error.append("{} :: is not in the valid name list \n Below are the valid naming convenction \n\n".format(i.name()))
                                error = True

                except Exception as e:
                    print (e)
                # with open(filepath, 'r') as nuke_file:
                #     line_count = 0
                #     for line in nuke_file:
                #         line_count += 1
                #         if re.match(FILE_SYSTEM_PATTERN, line):
                #             error = True
                #             print("Nuke script problem found in {} at line {}:\n{}".format(filepath, line_count, line.strip()))
            if not error:
                nuke.scriptClose(filepath)
                if verbose:
                    print("OK: {}".format(os.path.basename(filepath)))
            else:
                errors = True
        return errors

    # def get_names(self, show):
    #     naming_con = []
    #     path = os.path.join(os.path.dirname(__file__),'excel','{}.csv'.format(show))
    #
    #     with open(path) as f:
    #         data =list(csv.reader(f))
    #         for i in data:
    #             item = str(i).replace("['", '').replace("']", '')
    #             naming_con.append(item)
    #
    #     return naming_con

class MayaFilePackage(FileCheckerPackage):
    """Check Maya files integrity."""

    SCRIPT_NODE_PATTERN = re.compile(".*createNode script -n.*")
    VIRUS_PATTERN = re.compile("(.*vaccine_gene.*)|(.*breed_gene.*)")
    ASCII_EXTENSIONS = ('.ma', )

    def check_package(self, verbose=False):
        """
        Check package integrity.

        :param bool verbose: True for verbose output.

        :return: True if there there were errors, False otherwise.
        :rtype: bool
        """

        errors = False
        for filepath in self.files_to_check:
            error = False
            if os.path.splitext(filepath)[-1] in self.ASCII_EXTENSIONS:
                with open(filepath, 'r') as maya_file:
                    line_count = 0
                    for line in maya_file:
                        line_count += 1
                        if re.match(self.SCRIPT_NODE_PATTERN, line):
                            if re.match(self.VIRUS_PATTERN, line):
                                error = True
                                print("Maya virus pattern found in {} at line {}:\n{}".format(filepath, line_count, line.strip()))
            if not error:                                
                if verbose:
                    print("OK: {}".format(os.path.basename(filepath)))
            else:
                errors = True
        return errors


class OutsourcePackage(BasePackage):
    """Check package integrity."""
    PREPARE_CLASS = None

    def __init__(self, **kwargs):
        super(OutsourcePackage, self). __init__(**kwargs)
        assert self.PREPARE_CLASS
        self.prepare = self.PREPARE_CLASS()
    def check_package(self, verbose=False):
        return self.prepare.check_package(input_path = self.input_path,show = self.show, ptask = self.dept_type, path=self.package_path,sequences=self.sequences, standalone=self.standalone, verbose=verbose)


class PackageTracking():
    """Check tracking package integrity."""

    TEMPLATE_RE = re.compile('^(?P<scene>[A-Z0-9_]+)__(?P<shot>[A-Z0-9_]+)__(?P<plate>[A-Za-z0-9_]+)__(?P<task>.+)__(?P<label>[A-Za-z0-9_]+)__(?P<version>v[0-9]+)$')

    def __init__(self):
        self.wanted_sequence_exts = ('.exr', '.jpg', '.jpeg')
        self.wanted_standalone_exts = ('.3de', '.ma', '.nk', '.mel', '.obj', '.abc', '.exr', '.fbx','.mov')
        self.allowed_tasks = ('tracking', 'geo', 'rotomation','cameratrack', 'cam_mm', 'cones','ud_plate', 'locators', 'st_distort', 'st_undistort', 'cam_mm', 'cones', 'perspective', 'sphere', 'wireframe', 'camlineup','lensdistortion')
        self.ignore_files = ('.xls', '.xlsx', '.odt', '.txt', '.doc', '.docx')

    def check_package(self, sequences=None, standalone=None, verbose=False):
        """
        Check package integrity.

        :param list[str] sequences: file sequences to check.
        :param list[str] standalone: standalone files to check.
        :param bool verbose: True for verbose output.

        :return: True if there there were errors, False otherwise.
        :rtype: bool
        """

        if not all([sequences, standalone]):
            print('No files found.')
            return True
        else:
            file_sequences = sequences
            file_standalone = standalone
        error_string = []
        completed_files = []
        errors = False
        for cur_file in file_sequences + file_standalone:
            source_filepath = cur_file.__str__()
            extension = os.path.splitext(source_filepath)[-1]
            if extension in self.ignore_files:
                continue
            if extension not in self.wanted_sequence_exts + self.wanted_standalone_exts :
                print('Bad extension: \n\t{}\n\tExtension must be one of {}'.format(cur_file, str(self.wanted_sequence_exts + self.wanted_standalone_exts)))
                errors = True
                continue

            # Before doing any matching, make a brute force filepath validation
            is_generic_valid, fail_message = generic_filepath_validation(source_filepath)
            if not is_generic_valid:
                logger.warning('  is a Misfit file (bad naming -- generic): \n\t{}\n\t{}'.format(cur_file,
                                                                                                 fail_message))
                continue

            # Removing frames if any, and extension
            filename = os.path.basename(source_filepath).split('.')[0]
            match = self.TEMPLATE_RE.match(filename)
            splits = filename.split('__')
            if not match or len(splits) != 6:
                if len(splits) != 6:
                    error_string.append('Bad naming: \n\t{}'.format(cur_file))
                    errors = True
                    continue
                else:
                    scene, shot, plate, task, label, version = splits
            else:
                scene = match.group('scene')
                shot = match.group('shot')
                plate = match.group('plate')
                task = match.group('task')
                label = match.group('label')
                version = match.group('version')

            asset_type = 'sequences' if extension in self.wanted_sequence_exts else 'standalone'
            if task not in self.allowed_tasks:
                print('Bad task name "{}" in filename: \n\t{}\n\tTask name must be one of {}.'.format(task, cur_file, str(self.allowed_tasks)))
                errors = True
                continue

            if verbose:
                print("OK: {}".format(os.path.basename(source_filepath)))
        return errors


class PackageRotoPaint(BasePackage):
    """Check Rotopaint package integrity."""

    def __init__(self,**kwargs):
        self.wanted_sequence_exts = ('.exr', '.jpg', '.jpeg','.dpx')
        self.wanted_standalone_exts = ('.nk', '.sfx')
        self.allowed_tasks = ('paintcheck', 'rotocheck', 'cleanupcheck')
        self.ignore_files = ('.xls', '.xlsx', '.odt', '.txt', '.doc', '.docx')
        self.validate_plate_label_regex = r'(.*retime.*)|(.*_[vV]\d+.*)'

    def check_package(self,input_path= None,show = None,ptask= None, path = None, sequences=None, standalone=None, verbose=False):

        """
        Check package integrity.

        :param list[str] sequences: file sequences to check.
        :param list[str] standalone: standalone files to check.
        :param bool verbose: True for verbose output.

        :return: True if there there were errors, False otherwise.
        :rtype: bool
        """

        done_list = []
        if not ([sequences, standalone]):
            print('No files found.')
            return True
        else:
            file_sequences = sequences
            # file_standalone = standalone

        errors = False

        for cur_file in file_sequences:

            source_filepath = cur_file.__str__()
            pattern_path = os.path.relpath(source_filepath,os.path.dirname(path))

            show_atr = PROJECTS[show][ptask]
            input_shot = '_'.join(input_path.split('_')[:show_atr['input_split']])
            pattren = pattern_path.split('\\')
            print (len(pattren))
            if len(pattren) != show_atr['len_split']:

                roto_paint_error.append('Bad folder structure: \t{}\n\tPath must be {}\n\n'.format(pattern_path,'/shot_version_folder/<shot_task_folder>/<file_seq>'))
                errors = True

            if os.path.splitext(pattren[-1])[-1] != show_atr['file_format']:
                roto_paint_error.append(
                    'Bad filename extension: \n\t{}\n\t file must be match {}\n\n'.format(pattern_path,
                                                                                          show_atr['file_format']))
                errors = True



            #todo need to work on it
            if ptask == 'paint':
                if input_path != pattren[-1].split('.')[0]:
                    roto_paint_error.append('Bad file path: \t{}\n\tPath must match with {}\n\n'.format(pattern_path, pattren[-1].split('.')[0]))
                    errors = True

            if ptask != 'paint':
                print(ptask)
                shot, ver_task = pattren[-2].split(show_atr['task_split'])
                print(shot, ver_task)
                filename = pattren[-1].split('.')[0]
                ver, task = ver_task.split('_')

                if show == 'Manifest':
                    full_name = '{}_{}{}_{}'.format(input_shot, ptask, ver, task)

                else:
                    full_name = '{}_{}_{}_{}'.format(input_shot, ptask, ver, task)


                if filename != pattren[2].split('.')[0]:
                    roto_paint_error.append('Bad filename: \n\t{}\n\t file must be match with {}\n\n'.format(pattern_path, pattren[2]))
                    errors = True

                if full_name != pattren[2].split('.')[0]:
                    roto_paint_error.append(
                        'Bad shotname: \n\t{}\n\t Shot must be match with {}\n\n'.format(pattern_path, pattren[2]))
                    errors = True

                if pattren[-2] != pattren[-1].split('.')[0]:

                    roto_paint_error.append(
                        'Bad foldername: \n\t{}\n\t folder must be match with sequence{}\n\n'.format(pattern_path, pattren[2]))
                    errors = True



            done_list.append("OK: {}".format(os.path.basename(source_filepath)))
            if verbose:

                print("OK: {}".format(os.path.basename(source_filepath)))
        return errors,roto_paint_error, done_list


class PackageCompositing():
    """Check compositing package integrity."""

    TEMPLATE_RE = re.compile('^(?P<scene>[A-Z0-9_]+)__(?P<shot>[A-Z0-9_]+)__(?P<label>[a-zA-Z0-9_]+)__(?P<version>v[0-9]+)$')

    def __init__(self):
        self.wanted_sequence_exts = ('.exr', '.jpg', '.jpeg', '.tiff', '.tif')
        self.wanted_standalone_exts = ('.nk',)
        self.package_directory_task = "compositing"
        self.allowed_tasks = ('compositing',)
        self.ignore_files = ('.xls', '.xlsx', '.odt', '.txt', '.doc', '.docx')

    def check_package(self, sequences=None, standalone=None, verbose=False):
        """
        Check package integrity.

        :param list[str] sequences: file sequences to check.
        :param list[str] standalone: standalone files to check.
        :param bool verbose: True for verbose output.

        :return: True if there there were errors, False otherwise.
        :rtype: bool
        """

        if not all([a is not None for a in (sequences, standalone)]):
            print('No files found.')
            return True
        else:
            file_sequences = sequences
            file_standalone = standalone

        errors = False
        for cur_file in file_sequences + file_standalone:
            source_filepath = cur_file.__str__()
            extension = os.path.splitext(source_filepath)[-1].lower()
            if extension in self.ignore_files:
                continue
            if extension not in self.wanted_sequence_exts + self.wanted_standalone_exts:
                print('Bad extension: \n\t{}\n\tExtension must be one of {}'.format(cur_file, str(self.wanted_sequence_exts + self.wanted_standalone_exts)))
                errors = True
                continue

            tasks_found = re.search(self.package_directory_task, str(cur_file).lower())
            if tasks_found is None:
                print('Bad folder structure: \n\t{}'.format(cur_file))
                errors = True
                continue
            else:
                task = tasks_found.group(0)

            # Before doing any matching, make a brute force filepath validation
            is_generic_valid, fail_message = generic_filepath_validation(source_filepath)
            if not is_generic_valid:
                logger.warning('  is a Misfit file (bad naming -- generic): \n\t{}\n\t{}'.format(cur_file,
                                                                                                 fail_message))
                continue

            # Removing frame padding, if any, and extension
            filename = os.path.basename(source_filepath).split('.')[0]
            match = self.TEMPLATE_RE.match(filename)
            splits = filename.split('__')

            if not match or len(splits) != 4:
                print('Bad naming: \n\t{}'.format(cur_file))
                errors = True
                continue

            scene = match.group('scene')
            shot = match.group('shot')
            version = match.group('version')
            label = match.group('label')

            if task not in self.allowed_tasks:
                print('Bad task name "{}" in filename: \n\t{}\n\tTask name must be one of {}.'.format(task, cur_file, str(self.allowed_tasks)))
                errors = True
                continue

            if verbose:
                print("OK: {}".format(os.path.basename(source_filepath)))
        return errors


class TrackingPackage(OutsourcePackage):
    PREPARE_CLASS = PackageTracking


class RotoPaintPackage(OutsourcePackage):
    PREPARE_CLASS = PackageRotoPaint


class CompositingPackage(OutsourcePackage):
    PREPARE_CLASS = PackageCompositing
