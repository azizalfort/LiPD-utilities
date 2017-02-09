from .LiPD import LiPD
from ..helpers.directory import *
from ..helpers.loggers import create_logger

logger_lipd_lib = create_logger('LiPD_Library')


class LiPD_Library(object):
    """
    The LiPD Library is meant to encompass a collection of LiPD file objects that are being analyzed in the current
    workspace. The library holds one LiPD object for each LiPD file that is loaded.
    """

    def __init__(self):
        self.dir_root = ''
        # dir used to unpack all LiPD files to
        self.dir_tmp = create_tmp_dir()
        # master dictionary that will hold all lipd data, organized by dataset name
        self.master = {}
        logger_lipd_lib.info("LiPD Library created")

    # GET

    def get_dir(self):
        """
        DEPRECATED FUNCTION
        Get the dir_root value
        :return str: dir_root path
        """
        return self.dir_root

    def get_csv(self, name):
        """
        Get CSV data from LiPD file
        :param str name:
        :return dict:
        """
        d = {}
        try:
            d = self.master[name].get_csv()
        except KeyError:
            print("LiPD file not found")
        return d

    def get_metadata(self, name):
        """
        Get metadata from LiPD file
        :param str name:
        :return dict:
        """
        d = {}
        try:
            d = self.master[name].get_metadata()
        except KeyError:
            print("LiPD file not found")
        return d

    def get_dfs(self, name):
        """
        Get data frames from LiPD object
        :return dict:
        """
        d = {}
        try:
            d = self.master[name].get_dfs()
        except KeyError:
            logger_lipd_lib.debug("getDfs: KeyError: missing lipds {}".format(name))
        return d

    def get_master(self):
        """
        Retrieve the LiPD_Library master list. All names and LiPD objects.
        :return dict:
        """
        return self.master

    def get_lib_as_dict(self):
        """
        Return compiled dictionary of master data from all LiPDs in library.
        :return:
        """
        d = {}
        # for each dataset in the lipds library
        for k, v in self.master.items():
            # key is dataset name, value is master data
            d[k] = v.get_master()
        return d

    def get_lipd_names(self):
        """
        Get a list of all lipd dataset names in the library
        :return list:
        """
        f_list = []
        print("Found: {} file(s)".format(len(self.master)))
        for k, v in sorted(self.master.items()):
            f_list.append(k)
        return f_list

    # SHOW

    def show_csv(self, name):
        """
        Show CSV data from one LiPD object
        :param str name: Filename
        :return None:
        """
        try:
            self.master[name].display_csv()
        except KeyError:
            print("LiPD not found")
        return

    def show_metadata(self, name):
        """
        Display data from target LiPD file.
        :param str name: Filename
        :return None:
        """
        try:
            self.master[name].display_json()
        except KeyError:
            print("LiPD file not found")
        return

    def show_lipd_master(self, name):
        """
        Display data from target LiPD file.
        :param str name: Filename
        :return None:
        """
        try:
            self.master[name].display_master()
        except KeyError:
            print("LiPD not found")
        return

    def show_lipds(self):
        """
        Display all LiPD dataset names in the LiPD Library
        :return None:
        """
        print("Found: {} file(s)".format(len(self.master)))
        for k, v in sorted(self.master.items()):
            print(k)
        return

    # PUT

    def put_master(self, dat):
        """
        Put new data as the master dictionary
        :param dict dat:
        :return none:
        """
        self.master = dat
        return

    def set_dir(self, dir_root):
        """
        Changes the current working directory.
        :param str dir_root:
        :return:
        """
        try:
            self.dir_root = dir_root
            os.chdir(self.dir_root)
        except FileNotFoundError as e:
            logger_lipd_lib.debug("setDir: FileNotFound: invalid directory: {}, {}".format(self.dir_root, e))
        return

    # LOAD

    def read_lipd(self, file_meta):
        """
        Create and load a single LiPD object into the LiPD Library.
        :param dict file_meta: Filename
        :return None:
        """
        # file_meta =
        # {
        # "full_path"
        # "filename_ext",
        # "filename_no_ext",
        # "dir"
        # }
        os.chdir(file_meta["dir"])
        # create a lpd object
        lipd_obj = LiPD(file_meta["dir"], self.dir_tmp, file_meta["filename_ext"])
        # load in the data from the lipds file (unpack, and create a temp workspace)
        lipd_obj.load()
        # add the lpd object to the master dictionary
        self.master[file_meta["filename_ext"]] = lipd_obj
        return

    def load_tsos(self, d):
        """
        Overwrite converted TS metadata back into its matching LiPD object.
        :param dict d: Metadata from TSO
        """

        for name_ext, metadata in d.items():
            # Important that the dataSetNames match for TSO and LiPD object. Make sure
            try:
                self.master[name_ext].load_tso(metadata)
            except KeyError as e:
                print("Error loading " + str(name_ext) + " from TimeSeries object")
                logger_lipd_lib.warn("load_tsos: KeyError: failed to load {} from tso, {}".format(name_ext, e))

        return

    # SAVE

    def write_lipd(self, name):
        """
        Overwrite LiPD files in OS with LiPD data in the current workspace.
        """
        try:
            self.master[name].save()
            # Reload the newly saved LiPD file back into the library.
            self.read_lipd(name)
        except KeyError:
            print("LiPD file not found")
        return

    def write_lipds(self):
        """
        Overwrite target LiPD file in OS with LiPD data in the current workspace.
        """
        for k, v in self.master.items():
            self.master[k].save()
        return

    def remove_lipd(self, name):
        """
        Removes target LiPD file from the workspace. Delete tmp folder, then delete object.
        :param str name: Filename
        """
        try:
            self.master[name].remove()
            del self.master[name]
        except KeyError:
            print("LiPD file not found")
        return

    def remove_lipds(self):
        """
        Clear the workspace. Empty the master dictionary.
        """
        self.master = {}
        return


