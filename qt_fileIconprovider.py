import os

from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QFileIconProvider, QListWidgetItem


def add_file(self, filename):
    """
    Add a file or directory to this widget.
    """
    if filename not in self.filenames:
        self.filenames.append(filename)

        fileinfo = QFileInfo(filename)
        basename = os.path.basename(filename.rstrip('/'))
        ip = QFileIconProvider()
        icon = ip.icon(fileinfo)

        if os.path.isfile(filename):
            size = helpers.human_readable_filesize(fileinfo.size())
        else:
            size = helpers.human_readable_filesize(helpers.dir_size(filename))
        item_name = '{0:s} ({1:s})'.format(basename, size)
        item = QListWidgetItem(item_name)
        item.setToolTip(size)

        item.setIcon(icon)
        self.addItem(item)

        self.files_updated.emit()