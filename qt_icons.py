#!/usr/bin/env python
# coding: utf-8
# reference: https://unpyside.wixsite.com/unpyside/post/2017/10/16/%E3%80%90mayapyside%E3%80%91qt-%E3%81%A7%E4%BD%BF%E7%94%A8%E5%8F%AF%E8%83%BD%E3%81%AA%E7%B5%84%E3%81%BF%E8%BE%BC%E3%81%BF%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3%E4%B8%80%E8%A6%A7
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QIcon,
)
from PySide6.QtWidgets import (
    QApplication,
    QStyle,
    QSystemTrayIcon,
    QToolButton,
    QGridLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.Button()
        self.setWindowTitle('Qt icons')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def initUI(self):
        style = self.style()
        icon = style.standardIcon(QStyle.SP_TitleBarMenuButton)
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon(icon))
        self.setWindowIcon(QIcon(icon))

        for path in QIcon.themeSearchPaths():
            print("%s/%s" % (path, QIcon.themeName()))

    def Button(self):
        Styles = [
            QStyle.SP_TitleBarMinButton,
            QStyle.SP_TitleBarMenuButton,
            QStyle.SP_TitleBarMaxButton,
            QStyle.SP_TitleBarCloseButton,
            QStyle.SP_TitleBarNormalButton,
            QStyle.SP_TitleBarShadeButton,
            QStyle.SP_TitleBarUnshadeButton,
            QStyle.SP_TitleBarContextHelpButton,
            QStyle.SP_MessageBoxInformation,
            QStyle.SP_MessageBoxWarning,
            QStyle.SP_MessageBoxCritical,
            QStyle.SP_MessageBoxQuestion,
            QStyle.SP_DesktopIcon,
            QStyle.SP_TrashIcon,
            QStyle.SP_ComputerIcon,
            QStyle.SP_DriveFDIcon,
            QStyle.SP_DriveHDIcon,
            QStyle.SP_DriveCDIcon,
            QStyle.SP_DriveDVDIcon,
            QStyle.SP_DriveNetIcon,
            QStyle.SP_DirHomeIcon,
            QStyle.SP_DirOpenIcon,
            QStyle.SP_DirClosedIcon,
            QStyle.SP_DirIcon,
            QStyle.SP_DirLinkIcon,
            QStyle.SP_DirLinkOpenIcon,
            QStyle.SP_FileIcon,
            QStyle.SP_FileLinkIcon,
            QStyle.SP_FileDialogStart,
            QStyle.SP_FileDialogEnd,
            QStyle.SP_FileDialogToParent,
            QStyle.SP_FileDialogNewFolder,
            QStyle.SP_FileDialogDetailedView,
            QStyle.SP_FileDialogInfoView,
            QStyle.SP_FileDialogContentsView,
            QStyle.SP_FileDialogListView,
            QStyle.SP_FileDialogBack,
            QStyle.SP_DockWidgetCloseButton,
            QStyle.SP_ToolBarHorizontalExtensionButton,
            QStyle.SP_ToolBarVerticalExtensionButton,
            QStyle.SP_DialogOkButton,
            QStyle.SP_DialogCancelButton,
            QStyle.SP_DialogHelpButton,
            QStyle.SP_DialogOpenButton,
            QStyle.SP_DialogSaveButton,
            QStyle.SP_DialogCloseButton,
            QStyle.SP_DialogApplyButton,
            QStyle.SP_DialogResetButton,
            QStyle.SP_DialogDiscardButton,
            QStyle.SP_DialogYesButton,
            QStyle.SP_DialogNoButton,
            QStyle.SP_ArrowUp,
            QStyle.SP_ArrowDown,
            QStyle.SP_ArrowLeft,
            QStyle.SP_ArrowRight,
            QStyle.SP_ArrowBack,
            QStyle.SP_ArrowForward,
            QStyle.SP_CommandLink,
            QStyle.SP_VistaShield,
            QStyle.SP_BrowserReload,
            QStyle.SP_BrowserStop,
            QStyle.SP_MediaPlay,
            QStyle.SP_MediaStop,
            QStyle.SP_MediaPause,
            QStyle.SP_MediaSkipForward,
            QStyle.SP_MediaSkipBackward,
            QStyle.SP_MediaSeekForward,
            QStyle.SP_MediaSeekBackward,
            QStyle.SP_MediaVolume,
            QStyle.SP_MediaVolumeMuted,
            QStyle.SP_LineEditClearButton,
            #QStyle.SP_DialogYesToAllButton,
            #QStyle.SP_DialogNoToAllButton,
            #QStyle.SP_DialogSaveAllButton,
            #QStyle.SP_DialogAbortButton,
            #QStyle.SP_DialogRetryButton,
            #QStyle.SP_DialogIgnoreButton,
            #QStyle.SP_RestoreDefaultsButton,
            #QStyle.SP_CustomBase,
        ]

        StylesText = [
            'SP_TitleBarMinButton',
            'SP_TitleBarMenuButton',
            'SP_TitleBarMaxButton',
            'SP_TitleBarCloseButton',
            'SP_TitleBarNormalButton',
            'SP_TitleBarShadeButton',
            'SP_TitleBarUnshadeButton',
            'SP_TitleBarContextHelpButton',
            'SP_MessageBoxInformation',
            'SP_MessageBoxWarning',
            'SP_MessageBoxCritical',
            'SP_MessageBoxQuestion',
            'SP_DesktopIcon',
            'SP_TrashIcon',
            'SP_ComputerIcon',
            'SP_DriveFDIcon',
            'SP_DriveHDIcon',
            'SP_DriveCDIcon',
            'SP_DriveDVDIcon',
            'SP_DriveNetIcon',
            'SP_DirHomeIcon',
            'SP_DirOpenIcon',
            'SP_DirClosedIcon',
            'SP_DirIcon',
            'SP_DirLinkIcon',
            'SP_DirLinkOpenIcon',
            'SP_FileIcon',
            'SP_FileLinkIcon',
            'SP_FileDialogStart',
            'SP_FileDialogEnd',
            'SP_FileDialogToParent',
            'SP_FileDialogNewFolder',
            'SP_FileDialogDetailedView',
            'SP_FileDialogInfoView',
            'SP_FileDialogContentsView',
            'SP_FileDialogListView',
            'SP_FileDialogBack',
            'SP_DockWidgetCloseButton',
            'SP_ToolBarHorizontalExtensionButton',
            'SP_ToolBarVerticalExtensionButton',
            'SP_DialogOkButton',
            'SP_DialogCancelButton',
            'SP_DialogHelpButton',
            'SP_DialogOpenButton',
            'SP_DialogSaveButton',
            'SP_DialogCloseButton',
            'SP_DialogApplyButton',
            'SP_DialogResetButton',
            'SP_DialogDiscardButton',
            'SP_DialogYesButton',
            'SP_DialogNoButton',
            'SP_ArrowUp',
            'SP_ArrowDown',
            'SP_ArrowLeft',
            'SP_ArrowRight',
            'SP_ArrowBack',
            'SP_ArrowForward',
            'SP_CommandLink',
            'SP_VistaShield',
            'SP_BrowserReload',
            'SP_BrowserStop',
            'SP_MediaPlay',
            'SP_MediaStop',
            'SP_MediaPause',
            'SP_MediaSkipForward',
            'SP_MediaSkipBackward',
            'SP_MediaSeekForward',
            'SP_MediaSeekBackward',
            'SP_MediaVolume',
            'SP_MediaVolumeMuted',
            'SP_LineEditClearButton',
            #'SP_DialogYesToAllButton',
            #'SP_DialogNoToAllButton',
            #'SP_DialogSaveAllButton',
            #'SP_DialogAbortButton',
            #'SP_DialogRetryButton',
            #'SP_DialogIgnoreButton',
            #'SP_RestoreDefaultsButton',
            #'SP_CustomBase',
        ]

        btn = [QToolButton(self) for i in range(len(Styles))]

        self.myHLayout = QGridLayout()

        j = 0
        k = 0
        style = self.style()
        for i in range(len(Styles)):
            btn[i].setText("%s" % (StylesText[i]))
            btn[i].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            icon = style.standardIcon(Styles[i])
            btn[i].setIcon(QIcon(icon))

            self.myHLayout.addWidget(btn[i], j, k)

            if i == 0:
                pass
            elif 0 == i % 5:
                j += 1
                k = 0
            else:
                k += 1

        self.setLayout(self.myHLayout)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
