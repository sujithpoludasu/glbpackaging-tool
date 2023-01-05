
import sys
import os
import re
import posixpath
import argparse
import logging

from collections import defaultdict

from packages import ColouredLogger, MayaFilePackage, NukeFilePackage, TrackingPackage, RotoPaintPackage, CompositingPackage

logger = logging.getLogger(__name__)

PACKAGE_MAPPING = {'MatchMove': (TrackingPackage, MayaFilePackage, NukeFilePackage),
                  'paint': [RotoPaintPackage],
                  'roto': [RotoPaintPackage],
                  'Composting': (CompositingPackage, NukeFilePackage)
                  }


def create_parser():
    """
    Creates the argument parser to parse the command line arguments.

    :rtype argparse.ArgumentParser:
    """

    parser = argparse.ArgumentParser(prog='Package Sanity checker',
        description="Check package files before delivery to Client.")
    parser.add_argument('--type', '-t',
                        type=str, required=True, choices=PACKAGE_MAPPING.keys(),
                        help='Type of sanity-check to select : \n'
                             '{}'.format(PACKAGE_MAPPING.keys()))
    parser.add_argument('--path', '-p',
                        type=str, required=True, help='Path to the package to check')
    parser.add_argument('--verbose', '-v', action='store_true', default=False,
                        help='Optional: output files processed to console.')

    return parser


def collapseFramesToRanges(frames):
    """
    Takes in a list of frames and returns a string of minimal frame ranges/sequences e.g.:
        - [0,1,2,3,4,5] -> '0-5'
        - [1, 2, 3, 5] -> '1-3,5'

    :param list[int]|tuple[int]|set[int] frames: a list of integer castable frames, [0,1,2,3,4,5] or ['1','2','3']

    :rtype: str
    """
    assert hasattr(frames, '__iter__'), 'input paramater frames must be of iterable type, i.e. tuple, list not {type}'.format(type=frames.__class__.__name__)
    if len(frames) == 0:
        return ''

    frameString = ''
    prevFrame = None
    counting = False
    numFramesCounted = 0
    currInc, prevInc = None, None
    frames = sorted(list(set(frames)))  # sort and remove any duplicates

    for index in range(len(frames)):
        # cast to int, return empty string if anything other than an int has been passed in
        try:
            currFrame = int(frames[index])
        except:
            return ''

        # if no prevFrame, add yourself to frameString, start counting
        if prevFrame == None:
            if frameString:
                frameString += ','
            frameString += str(currFrame)
            counting = True
        # otherwise, set currInc amount
        else:
            currInc = currFrame - prevFrame

            # if there's no prevInc value, increment numFramesCounted to 1 (we have counted one past original value)
            if prevInc == None:
                counting = True
                numFramesCounted += 1
            # we have two values behind us, check to see if our increment is staying the same
            # if increment value has not changed, keep going
            elif currInc == prevInc:
                counting = True
                numFramesCounted += 1
            # if increment value is changing, add previous value
            elif counting:
                frameString += ('-' if numFramesCounted > 1 else ',')
                frameString += str(prevFrame)

                # add x-notation if necessary
                if prevInc != 1 and numFramesCounted > 1:
                    frameString += 'x' + str(prevInc)

                if numFramesCounted > 1:
                    frameString += ',' + str(currFrame)
                    numFramesCounted = 1
                    counting = False

        # we are the last element
        if index == len(frames) - 1 and len(frames) > 1:
            stringToAdd = ''
            if numFramesCounted > 1:
                stringToAdd += '-' + str(currFrame)
                if currInc != 1:
                    stringToAdd += 'x' + str(currInc)
            elif prevFrame == None or prevFrame != currFrame:
                stringToAdd += ',' + str(currFrame)

            if not frameString.endswith(stringToAdd) or frameString == stringToAdd:
                frameString += stringToAdd

        # update state variables
        prevFrame = currFrame
        prevInc = currInc if counting else None
        if not counting:
            numFramesCounted = 0

    return frameString


def parseFrameString(frameString):
    """
    Parses a frame string and returns a frame range and a list of bad syntax
    The bad syntax is a pointer into the group of , separated strings e.g.:
    - '1-4' -> [1,2,3,4], []
    - '-1-1' -> [-1,0,1], []
    - '-3--1' -> [-3,-2,-1], []
    - '1-2,4-3' -> [1,2], [1] so bad syntax is '1-2,4-3'.split(',')[1]

    :param str frameString: a string representing the frames, '1-4', '1,3,5', '1-10x2'

    :rtype: tuple[list[int], list[int]]
    :returns: a sorted list of frame integers and bad syntax indices, ([1,2,3,4], []), ([1,3,5], []), ([2,4,6,8,10], [])
    """
    frames = []
    badSyntaxChunks = []

    pattern = re.compile(r'\(([0-9]+)\)')
    matches = pattern.findall(frameString)
    if len(matches) > 0:
        for match in matches:
            frameString = frameString.replace('(%s)' % match.strip(), '')

    for index, chunk in enumerate(frameString.split(',')):
        # Kill whitespace, make lowercase, remove all non-numerical or non-dash/non-'x' chars
        chunk = re.sub(r'[^0-9-x]', ' ', chunk.strip().lower())

        # Any mutliple x's get reduced to singles
        chunk = re.sub(r'x+', 'x', chunk)
        # More than 2 '-'s in a row become just '--'
        chunk = re.sub(r'--+', '--', chunk)
        # Double dashes at beginning of string become '-' (single negative)
        chunk = re.sub(r'^--*', '-', chunk)

        # Skip this chunk if there are any spaces between two numbers, or more than 7 digits in a row, or chunk is blank
        if re.search(r'\d\s+\d|\d{8,}', chunk):
            badSyntaxChunks.append(index)
            continue
        # Continue, but don't add to badSyntax for chunk==''; this will allow for dangling ,'s (index.e. '1-10,')
        elif chunk == '':
            continue

        # Step frames desired
        if 'x' in chunk:
            # Ignore if there's no proper frameRange
            if not '-' in chunk:
                badSyntaxChunks.append(index)
                continue

            frameRange = chunk.split('x')[0]
            if len(chunk.split('x')) == 2 and not chunk.split('x')[1] == '':
                frameInc = cleanFrameNumber(chunk.split('x')[1])
            # If there's a dangling x (index.e. '2-24x'), assume frameInc = 1
            else:
                frameInc = 1

            if not frameInc:
                badSyntaxChunks.append(index)
                continue

            if '--' in frameRange:
                frameChunks = frameRange.split('--')
                # negate second frameChunk, as we dropped it's negative above
                num = cleanFrameNumber(frameChunks[1])
                if num == None:
                    badSyntaxChunks.append(index)
                    continue
                frameChunks[1] = str(-1 * num)
            else:
                frameChunks = frameRange.rsplit('-', 1)

            if not len(frameChunks) == 2 or frameInc < 0:
                badSyntaxChunks.append(index)
                continue

            startFrame = cleanFrameNumber(frameChunks[0])
            endFrame = cleanFrameNumber(frameChunks[1])

            if not startFrame or not endFrame:
                badSyntaxChunks.append(index)
                continue

            (seqFrames, badSyntax) = getFramesInRange(startFrame, endFrame, frameInc)
            if badSyntax:
                badSyntaxChunks.append(index)
                continue
            frames.extend(seqFrames)

        # consecutive frames desired, multiple frames in this chunk, no single negative frames
        elif '-' in chunk and not re.search('^-[0-9]*$', chunk):
            frameInc = 1

            if '--' in chunk:
                frameChunks = chunk.split('--')
                # negate second frameChunk, as we dropped it's negative above
                frameChunks[1] = '-' + frameChunks[1]
            else:
                frameChunks = chunk.rsplit('-', 1)

            startFrame = cleanFrameNumber(frameChunks[0])
            endFrame = cleanFrameNumber(frameChunks[1])

            if startFrame is None:
                badSyntaxChunks.append(index)
                continue
            # if there's only a startFrame, add it and continue
            elif not endFrame:
                frames.append(startFrame)
                continue

            (seqFrames, badSyntax) = getFramesInRange(startFrame, endFrame, frameInc)
            if badSyntax:
                badSyntaxChunks.append(index)
                continue

            frames.extend(seqFrames)

        # only one frame in this chunk
        else:
            frame = cleanFrameNumber(chunk)
            if not frame:
                badSyntaxChunks.append(index)
                continue

            frames.append(frame)

    return sorted(list((set(frames)))), sorted(list((set(badSyntaxChunks))))


def cleanFrameNumber(frame):
    """ Cleans frame number by stripping Non-Numerical, Non-Minus-Sign characters, trailing minues or multiple minuses

        :param str input: the frame string to be cleaned
        :returns string: returns None on error
    """
    try:
        frame = frame.strip()
        if re.search('[^0-9-]', frame):
            return None

        # Remove non-numerical or non-minus sign chars, remove trailing minus signs, multiple minus signs become one
        frame = re.sub('[^0-9-]', ' ', frame)
        frame = re.sub('-+$', '', frame)
        frame = re.sub('-+', '-', frame)

        frame = int(frame)
    except:
        return None

    return frame


def getFramesInRange(startFrame, endFrame, frameInc):
    """ Creates a list of all frames in a range, frame values are inclusive e.g.:
        - 1,3,1 -> 1,2,3
        - 2,10,2 -> 2,4,6,8,10

        :param int startFrame: the start frame, eg. 1
        :param int endFrame: the end frame, eg. 3
        :param int frameInc: the frame step, eg. 1

        :returns a list of frames, a boolean value whether there was bad syntax

    """
    frames = []
    badSyntax = False

    # ensure that an empty list is return if startFrame > endFrame
    if startFrame <= endFrame and frameInc > 0:
        currFrame = startFrame
        while currFrame <= endFrame:
            frames.append(currFrame)
            currFrame += frameInc
    else:
        return [], True

    return frames, badSyntax


# regular expression for determining whether a file is part of a file sequence
SEQ_RE = re.compile(r"^(?P<file_prefix>.+\.)(?P<frame>\d+)(?P<suffix>(\.[a-zA-Z0-9_]+)?(\.(sc|tmp|exr))?)$")
TEMPLATE_RE = re.compile(r"^(?P<file_prefix>.*)(?P<frame>%(?P<pad>-?\d*)d)(?P<suffix>.*)$")


class FileSequence(object):
    """ Contains a single file sequence and relevant attributes

    **Example:**
        seq = FileSequence(directory="/tmp/foo", file_prefix="filename", suffix="exr", pad=4)

        FileSequence objects are normally created with the get_sequences() and create_sequence() functions.

    :type str directory: The directory path to the sequence
    :type str file_prefix: Everything on the filename preceding the frame number
    :type str suffix: Everything after the frame number
    :type int pad: The number of digits of padding used
    :type set[int] frames:
    """

    # Conventions for representing frame padding
    CONV_CPRINTF, CONV_SHAKE, CONV_HOUDINI, CONV_HASH = range(4)

    def __init__(self, directory="", file_prefix="", suffix="", pad=0):
        """
        :param str directory:
        :param str file_prefix:
        :param str suffix:
        :param int pad:
        """
        self.directory = directory
        self.file_prefix = file_prefix
        self.suffix = suffix
        self.pad = pad
        self.frames = set()

    def get_frame_path(self, frame):
        """ Returns the full path to the given frame

        :param int frame: The frame number to return the path for

        :returns: string
        """
        if self.pad > -1:
            return self.template % frame
        else:
            return self.template

    def get_template(self, convention):
        """ Returns the sequence filepath using the given frame padding convention

        :param enum convention: The naming convention to use; one of the following:
        * FileSequence.CONV_CPRINTF - Use cprintf-stype formatting; this is the default.
        * FileSequence.CONV_SHAKE - Use Shake-style formatting, with @ representing a single digit
        * FileSequence.CONV_HOUDINI - Use Houdini-style formatting
        * FileSequence.CONV_HASH - Use a hash character to denote the frame number

        :returns: string
        """
        if convention == FileSequence.CONV_HASH:
            return self.prefix + '#' + self.suffix
        elif convention == FileSequence.CONV_SHAKE:
            return self.prefix + ('@' * self.pad if self.pad > 0 else '@') + self.suffix
        elif convention == FileSequence.CONV_HOUDINI:
            return self.prefix + '$F' + (str(self.pad) if self.pad > 0 else '') + self.suffix
        else:
            return self.template

    def add_frame(self, frame):
        """ Add a single frame to the current FileSequence

        :param string frame: The full path to a frame in the sequence.

        The given filepath must match that of the existing sequence, or it will get ignored.
        """
        match = re.match(self.regex, frame)
        if match:
            self.frames.add(int(match.group('frame')))

    def limit(self, start=None, end=None):
        """ Truncates the frame range to the given start/end values (preserving any gaps in the existing range)

        :param int start: the first frame of the new frame range (optional)
        :param int end: the last frame of the new frame range (optional)

        Note that this method will do nothing if neither argument is given, or if the given range is larger than the
        existing one.
        """
        if self.bounds:
            if not start:
                start = self.bounds[0]
            if not end:
                end = self.bounds[-1]
        limit_range = set(range(start, end + 1))
        self.frames = self.frames.intersection(limit_range)

    @property
    def padding_token(self):
        """
        Returns a properly formatted padding token.

        :rtype: str
        """
        return r'%{}d'.format('%02d' % self.pad)

    @property
    def basename(self):
        """
        Returns a serialized version of sequence basename.
        This will concatenate file name, padding and extension.

        :rtype: str
        """
        return str(self.file_prefix + self.padding_token + self.suffix)

    @property
    def regex(self):
        """ Returns a regular expression to test for sequence membership
        :returns: a regular expression string
        """
        escaped_regex = set(['^', '$', '(', ')', '<', '[', '{', '\\', '|', '>', '.', '*', '+', '?'])

        prefix = self.prefix
        if set(prefix) & escaped_regex:
            for escaped in set(prefix) & escaped_regex:
                prefix = prefix.replace(escaped, r'\%s' % escaped)

        suffix = self.suffix
        if set(suffix) & escaped_regex:
            for escaped in set(suffix) & escaped_regex:
                suffix = suffix.replace(escaped, r'\%s' % escaped)

        if self.pad == 0:
            return '^' + prefix + r'(?P<frame>-?\d+)' + suffix + '$'
        elif self.pad > -1:
            return '^' + prefix + r'(?P<frame>-?\d{' + str(self.pad) + '})' + suffix + '$'
        else:
            return '^' + prefix + '(?P<frame>)' + suffix + '$'

    @property
    def template(self):
        """ Returns the cprintf-formatted path to the sequence
        :returns: a cprintf-formatted string
        """
        if self.pad == 0:
            return self.prefix + "%d" + self.suffix
        elif self.pad > -1:
            return self.prefix + "%0" + str(self.pad) + "d" + self.suffix
        else:
            return self.prefix + self.suffix

    @property
    def size(self):
        """ Returns the number of items in the sequence
        :returns: int
        """
        return len(self.frames)

    @property
    def prefix(self):
        """ Returns the entire filepath prior to the frame number
        :returns: string
        """
        return posixpath.join(self.directory, self.file_prefix)

    @property
    def gaps(self):
        """ Returns a list of gaps in the frame range
        :returns: list
        """
        if not self.frames:
            return []
        frames = sorted(self.frames)
        full_range = set(range(frames[0], frames[-1]))
        return list(full_range - self.frames)

    @property
    def bounds(self):
        """ Returns the first and last frames of the sequence

        :returns: tuple containing the first and last frame numbers, or None if the sequence is empty
        :rtype: tuple[int, int]|None
        """
        if self.frames:
            frames = sorted(self.frames)
            return frames[0], frames[-1]

    @property
    def resolution(self):
        """
        Returns the resolution of the FileSequence as a string or None if no resolution found in the path name.
        :rtype: str|None
        """
        re_res = re.search(r'(/\d{1,5})x(\d{1,5}/)', self.get_template(0))
        return re_res.group(0)[1:-1] if re_res else None

    @property
    def owner(self):
        """
        Assume entire sequence is owned by the same user, only check ownership on
        first frame of the sequence to make things faster.
        :rtype: str
        """
        if not self.frames:
            return ''
        first_frame = sorted(self.frames)[0]
        return pwd.getpwuid(os.stat(self.get_frame_path(first_frame)).st_uid).pw_name

    # Operators
    def __str__(self):
        """ Returns the template, or if the sequence consists of a single frame, simply returns the path
        """
        if len(self.frames) == 1:
            return self.template % list(self.frames)[0]
        else:
            return self.template

    def __hash__(self):
        return hash(self.__str__())

    def __iter__(self):
        """ Iterates through each filepath in the FileSequence, in order
        """
        frames = sorted(self.frames)
        for f in frames:
            yield self.get_frame_path(f)

    def __eq__(self, other):
        """ Objects are equal if all naming attributes match up. The specific frame ranges may differ.

        :param FileSequence other: The object being compared against
        """
        if isinstance(other, FileSequence):
            return ((self.directory == other.directory) and
                    (self.file_prefix == other.file_prefix) and
                    (self.suffix == other.suffix) and
                    (self.pad == other.pad))
        return False

    def __ne__(self, other):
        """ Objects are not equal of any of the naming attributes do not line up.

        :param FileSequence other: The object being compared against
        """
        if isinstance(other, FileSequence):
            return ((self.directory != other.directory) or
                    (self.file_prefix != other.file_prefix) or
                    (self.suffix != other.suffix) or
                    (self.pad != other.pad))
        return True

    def __iadd__(self, other):
        """ Only works for matching (equal) FileSequence objects; adds the other object's frame range to self

        :param FileSequence other: The object to add

        :raises: SequenceError if the sequences are not equal
        """
        if self != other:
            raise SequenceError("Incompatible sequences!")
        self.frames.update(other.frames)
        return self

    def __len__(self):
        """ Returns the number of frames

        :returns: int
        """
        return self.size

    def __getitem__(self, i):
        """ Returns the filepath at the given index. Note that the frame number will not necessarily match the given index

        :param int i: The i'th item in the ordered list of files is returned

        :raises: IndexError if the index is not within the frame bounds
        """
        frames_list = list(self.frames)
        frames_list.sort()
        try:
            frame = frames_list[i]
        except IndexError:
            raise IndexError('Given index is outside the sequence range (%s)' % len(self))
        return self.get_frame_path(frame)

    @property
    def frames_str(self):
        """ Returns a string representation of the frame range
        """
        return collapseFramesToRanges(self.frames)

    def serialize(self):
        """ Returns a string representation of the object
        """
        if self.pad < 0:
            return "{0.prefix}%{0.pad}d{0.suffix}:{0.frames_str}".format(self)
        return "{0.template}:{0.frames_str}".format(self)

    @classmethod
    def deserialize(cls, s):
        """ Returns a FileSequence object based on the serialised string s

        :param string s: A serialised FileSequence

        :returns: A new FileSequence object

        :raises SequenceError: On failure to parse  s
        """
        parts = s.split(':')
        if len(parts) != 2:
            raise SequenceError("Malformed string {0} (must contain : between template and frame range)".format(s))
        template, frame_range = parts
        directory, filename = os.path.split(template)
        match = TEMPLATE_RE.match(filename)
        if not match:
            raise SequenceError("String not is not a valid sequence filename: {0}".format(filename))
        frames, invalid = parseFrameString(frame_range)
        if len(invalid) > 0:
            raise SequenceError("Malformed frame range string {0} (index {1})".format(frame_range, invalid))

        new_seq = FileSequence(directory=directory,
                               file_prefix=match.group('file_prefix'),
                               suffix=match.group('suffix'),
                               pad=int(match.group('pad')) if match.group('pad') else 0)
        new_seq.frames = set(frames)
        return new_seq

    def startswith(self, string):
        """
        :param string: prefix string
        :return: Bool
        """
        return str(self).startswith(string)


def get_sequences(directory, depth=0, expr=None):
    """
    Generates sequence objects from the given directory.

    **Example:**
        # return all sequences directly within /tmp/foo with filenames matching the expression "bar.+"
        sequences, leftovers = get_sequences('/tmp/foo', expr="bar.+")
        # recursively scan /tmp/foo for all file sequences
        sequences, leftovers = get_sequences('/tmp/foo', depth=-1)

    :param str directory: The root directory to scan
    :param int depth: Recursively scan to the given depth,
                      or until the tree is exhausted when set to -1 (only scans the given directory by default)
    :param str expr: A regular expression to filter files with (optional)

    :returns: a tuple containing sequence objects and non-sequence filepaths
    :rtype: tuple[list[FileSequence], list[str]]
    """
    dirs, files = list(), list()
    if not os.path.exists(directory):
        return dirs, files
    if expr:
        expr = re.compile(expr)
    for f in os.listdir(directory):
        filepath = posixpath.join(directory, f)
        if os.path.isdir(filepath):
            dirs.append(filepath)
        elif not expr or expr.match(f):
            files.append(filepath)
    sequences, standalones = get_sequences_from_paths(files)
    if (depth > 0) or (depth < 0):
        for d in dirs:
            sub_sequences, sub_standalones = get_sequences(d, depth=depth - 1, expr=expr)
            sequences.extend(sub_sequences)
            standalones.extend(sub_standalones)
    return sequences, standalones


def get_sequences_from_paths(filepaths):
    """
    Generates sequence objects from given string iterable

    :param iterable filepaths: An iterable object returning path strings

    Note: Sequences which begin with a frame which fills the padding (no leading 0's) are assumed to be unpadded (pad = 1)
    Note: When a padded and an unpadded sequence converge, the padded sequence is favoured

    :returns: 2-tuple containing a list of FileSequence objects, a list of unmatched strings
    :rtype: tuple[list[FileSequence], list[str]]
    """
    seq_grps, unmatched = defaultdict(dict), list()
    # Sort given filepaths.
    for filepath in sorted(filepaths):
        path, filename = posixpath.split(filepath)
        seq_match = SEQ_RE.match(filename)
        if not seq_match:
            unmatched.append(filepath)
        else:
            # Group matching file sequences/padding.
            seq_key = '{0}/{1}#{2}'.format(path, seq_match.group('file_prefix'), seq_match.group('suffix'))
            padding = len(seq_match.group('frame'))
            if seq_key not in seq_grps or padding not in seq_grps[seq_key]:
                seq_grps[seq_key][padding] = FileSequence(directory=path,
                                                          file_prefix=seq_match.group('file_prefix'),
                                                          pad=padding,
                                                          suffix=seq_match.group('suffix'))
            seq = seq_grps[seq_key][padding]
            seq.frames.add(int(seq_match.group('frame')))
    # Compress, non-overlapping, sequences.
    sequences = list()
    for seq_key in seq_grps:
        # Loop grouped sequence padding from longest down.
        paddings = sorted(seq_grps[seq_key].keys(), reverse=True)
        parent_pad_idx = 0
        while parent_pad_idx < len(paddings):
            parent_pad = paddings[parent_pad_idx]
            parent_seq = seq_grps[seq_key][parent_pad]

            # Add sequence to final list and increment idx for next pass.
            sequences.append(parent_seq)
            parent_pad_idx += 1

            # Loop related sequences.
            child_pad_idx = parent_pad_idx
            while child_pad_idx < len(paddings):
                child_pad = paddings[child_pad_idx]
                child_seq = seq_grps[seq_key][child_pad]

                # Skip merge if sequence min frame len is less than sequence padding
                # e.g. padding = %04d but first frame is 950, so file would be 0950.
                if len(str(min(parent_seq.frames))) == child_pad:
                    break

                # Break if sequences have overlapping frame ranges.
                if set(parent_seq.frames).intersection(child_seq.frames):
                    break

                # Update padding to be shortest, %03d works for <= 999 and >= 1000
                parent_seq.pad = child_pad
                # Add frames.
                parent_seq.frames.update(child_seq.frames)

                # Increment idxs for next pass.
                parent_pad_idx += 1
                child_pad_idx += 1

    return sequences, unmatched


def get_package_name_from_path(path):
    """
    We assume that path is the exact root directory of the package. In addition to extracting the base dir name, we
    account for the possibility that it is prefixed with `data_packages__` (i.e. if run internally in CS)

    :param path: base fullpath to package
    :return: str
    """
    bn = os.path.basename(path)

    # data_package__ is expected to be lowercase
    return bn.split('data_package__')[-1]


def validate_package_name(package_name):
    """
    Validate the package name. All packages must conform to the CS standard of:

        {site}_{date}_{show}_{vendor}_OS_{task}_{upload-num}

    If for any reason CS has provided a spec sheet that is different from the above, please confirm, and ignore the
    results from this validation if applicable.

    :param str package_name: package name
    :return: bool
    """
    validation_regex = r'(?P<site>LDN|MTL)_(?P<date>\d+)_(?P<show>\w+)_(?P<vendor>\w+)_OS_(?P<task>\w+)_(?P<upload_num>\d+)'

    result = re.match(validation_regex, package_name)
    return bool(result)


def main(src, out,dst, dept_type, show):

    package_sequences, package_standalone = get_sequences(out, depth=-2)


    # print (package_sequences)
    # Validate the package name
    # package_name = get_package_name_from_path(args.path)

    errors = []
    for package_type in PACKAGE_MAPPING[dept_type]:
        package = package_type(input_path = src,
                               show = show,
                               dept_type = dept_type,
                               pack_path=out,
                               sequences=package_sequences,
                               standalone=package_standalone)
        errors.append(package.check_package(verbose=True))

    # is_valid_package_name = validate_package_name(package_name)
    #
    # if not is_valid_package_name:
    #     msg = 'Package name "{}" is not valid.'.format(package_name)
    #     errors.append(msg)
    #     logger.error(msg)
    # print (errors)
    #
    # if True in errors[0]:
    #     logger.error("Check complete. Errors were found in the package.")
    #     logger.error("See all the details above to fix the issues.")
    #     logger.error("Please do not submit the package until the issues are fixed.")
    # else:
    #     logger.info("Check complete.")
    #     logger.info("No errors found. The package can be submitted.")
    return errors


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
