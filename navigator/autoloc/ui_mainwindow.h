/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.5.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QPushButton *worldBtn;
    QLabel *cameraLbl;
    QGroupBox *tempFusionGrp;
    QRadioButton *kalmanRdb;
    QCheckBox *tempFusionChk;
    QRadioButton *weightRdb;
    QPushButton *errorBtn;
    QLabel *label;
    QLabel *label_9;
    QLabel *label_10;
    QLabel *label_11;
    QLabel *label_12;
    QLabel *label_13;
    QLabel *label_2;
    QLabel *label_14;
    QLabel *label_3;
    QLineEdit *lineEdit;
    QLineEdit *xEstimTxt;
    QLineEdit *xErrorTxt;
    QLineEdit *lineEdit_4;
    QLineEdit *yEstimTxt;
    QLineEdit *yErrorTxt;
    QLineEdit *lineEdit_7;
    QLineEdit *zEstimTxt;
    QLineEdit *pitchErrorTxt;
    QLineEdit *pitchEstimTxt;
    QLineEdit *lineEdit_11;
    QLineEdit *rollErrorTxt;
    QLineEdit *rollEstimTxt;
    QLineEdit *lineEdit_14;
    QLineEdit *zErrorTxt;
    QLineEdit *yawEstimTxt;
    QLineEdit *yawErrorTxt;
    QLineEdit *yawRealTxt;
    QLabel *label_4;
    QLabel *label_5;
    QLineEdit *radialErrorTxt;
    QLineEdit *angularErrorTxt;
    QLineEdit *pitchRealTxt;
    QLineEdit *xRealTxt;
    QLineEdit *yRealTxt;
    QLineEdit *zRealTxt;
    QLineEdit *rollRealTxt;
    QCheckBox *realMarkerChk;
    QCheckBox *arDemoChk;
    QLineEdit *corner0Txt;
    QLineEdit *corner2Txt;
    QLineEdit *corner1Txt;
    QLineEdit *corner3Txt;
    QLabel *label_6;
    QLineEdit *markerIdTxt;
    QPushButton *copyBtn;
    QPushButton *plusBtn;
    QPushButton *minusBtn;
    QGroupBox *tempFusionGrp_2;
    QRadioButton *xRdb;
    QRadioButton *yRdb;
    QRadioButton *zRdb;
    QRadioButton *rollRdb;
    QRadioButton *pitchRdb;
    QRadioButton *yawRdb;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(520, 800);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        worldBtn = new QPushButton(centralWidget);
        worldBtn->setObjectName(QStringLiteral("worldBtn"));
        worldBtn->setGeometry(QRect(20, 620, 481, 41));
        cameraLbl = new QLabel(centralWidget);
        cameraLbl->setObjectName(QStringLiteral("cameraLbl"));
        cameraLbl->setGeometry(QRect(20, 10, 480, 360));
        cameraLbl->setFrameShape(QFrame::Box);
        cameraLbl->setScaledContents(true);
        cameraLbl->setAlignment(Qt::AlignHCenter|Qt::AlignTop);
        tempFusionGrp = new QGroupBox(centralWidget);
        tempFusionGrp->setObjectName(QStringLiteral("tempFusionGrp"));
        tempFusionGrp->setGeometry(QRect(20, 670, 321, 61));
        kalmanRdb = new QRadioButton(tempFusionGrp);
        kalmanRdb->setObjectName(QStringLiteral("kalmanRdb"));
        kalmanRdb->setEnabled(false);
        kalmanRdb->setGeometry(QRect(10, 30, 116, 22));
        kalmanRdb->setChecked(false);
        tempFusionChk = new QCheckBox(tempFusionGrp);
        tempFusionChk->setObjectName(QStringLiteral("tempFusionChk"));
        tempFusionChk->setEnabled(true);
        tempFusionChk->setGeometry(QRect(120, 0, 21, 22));
        tempFusionChk->setChecked(false);
        weightRdb = new QRadioButton(tempFusionGrp);
        weightRdb->setObjectName(QStringLiteral("weightRdb"));
        weightRdb->setEnabled(false);
        weightRdb->setGeometry(QRect(120, 30, 161, 22));
        weightRdb->setChecked(true);
        errorBtn = new QPushButton(centralWidget);
        errorBtn->setObjectName(QStringLiteral("errorBtn"));
        errorBtn->setGeometry(QRect(20, 580, 481, 31));
        label = new QLabel(centralWidget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(10, 490, 71, 17));
        label_9 = new QLabel(centralWidget);
        label_9->setObjectName(QStringLiteral("label_9"));
        label_9->setGeometry(QRect(230, 430, 16, 17));
        label_10 = new QLabel(centralWidget);
        label_10->setObjectName(QStringLiteral("label_10"));
        label_10->setGeometry(QRect(280, 430, 31, 17));
        label_11 = new QLabel(centralWidget);
        label_11->setObjectName(QStringLiteral("label_11"));
        label_11->setGeometry(QRect(340, 430, 41, 17));
        label_12 = new QLabel(centralWidget);
        label_12->setObjectName(QStringLiteral("label_12"));
        label_12->setGeometry(QRect(400, 430, 31, 17));
        label_13 = new QLabel(centralWidget);
        label_13->setObjectName(QStringLiteral("label_13"));
        label_13->setGeometry(QRect(110, 430, 16, 17));
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(40, 460, 31, 17));
        label_14 = new QLabel(centralWidget);
        label_14->setObjectName(QStringLiteral("label_14"));
        label_14->setGeometry(QRect(170, 430, 16, 17));
        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(40, 520, 41, 17));
        lineEdit = new QLineEdit(centralWidget);
        lineEdit->setObjectName(QStringLiteral("lineEdit"));
        lineEdit->setGeometry(QRect(90, 450, 51, 27));
        xEstimTxt = new QLineEdit(centralWidget);
        xEstimTxt->setObjectName(QStringLiteral("xEstimTxt"));
        xEstimTxt->setEnabled(false);
        xEstimTxt->setGeometry(QRect(90, 480, 51, 27));
        xEstimTxt->setReadOnly(true);
        xErrorTxt = new QLineEdit(centralWidget);
        xErrorTxt->setObjectName(QStringLiteral("xErrorTxt"));
        xErrorTxt->setEnabled(false);
        xErrorTxt->setGeometry(QRect(90, 510, 51, 27));
        xErrorTxt->setReadOnly(true);
        lineEdit_4 = new QLineEdit(centralWidget);
        lineEdit_4->setObjectName(QStringLiteral("lineEdit_4"));
        lineEdit_4->setGeometry(QRect(150, 450, 51, 27));
        yEstimTxt = new QLineEdit(centralWidget);
        yEstimTxt->setObjectName(QStringLiteral("yEstimTxt"));
        yEstimTxt->setEnabled(false);
        yEstimTxt->setGeometry(QRect(150, 480, 51, 27));
        yEstimTxt->setReadOnly(true);
        yErrorTxt = new QLineEdit(centralWidget);
        yErrorTxt->setObjectName(QStringLiteral("yErrorTxt"));
        yErrorTxt->setEnabled(false);
        yErrorTxt->setGeometry(QRect(150, 510, 51, 27));
        yErrorTxt->setReadOnly(true);
        lineEdit_7 = new QLineEdit(centralWidget);
        lineEdit_7->setObjectName(QStringLiteral("lineEdit_7"));
        lineEdit_7->setGeometry(QRect(210, 450, 51, 27));
        zEstimTxt = new QLineEdit(centralWidget);
        zEstimTxt->setObjectName(QStringLiteral("zEstimTxt"));
        zEstimTxt->setEnabled(false);
        zEstimTxt->setGeometry(QRect(210, 480, 51, 27));
        zEstimTxt->setReadOnly(true);
        pitchErrorTxt = new QLineEdit(centralWidget);
        pitchErrorTxt->setObjectName(QStringLiteral("pitchErrorTxt"));
        pitchErrorTxt->setEnabled(false);
        pitchErrorTxt->setGeometry(QRect(330, 510, 51, 27));
        pitchErrorTxt->setReadOnly(true);
        pitchEstimTxt = new QLineEdit(centralWidget);
        pitchEstimTxt->setObjectName(QStringLiteral("pitchEstimTxt"));
        pitchEstimTxt->setEnabled(false);
        pitchEstimTxt->setGeometry(QRect(330, 480, 51, 27));
        pitchEstimTxt->setReadOnly(true);
        lineEdit_11 = new QLineEdit(centralWidget);
        lineEdit_11->setObjectName(QStringLiteral("lineEdit_11"));
        lineEdit_11->setGeometry(QRect(330, 450, 51, 27));
        rollErrorTxt = new QLineEdit(centralWidget);
        rollErrorTxt->setObjectName(QStringLiteral("rollErrorTxt"));
        rollErrorTxt->setEnabled(false);
        rollErrorTxt->setGeometry(QRect(270, 510, 51, 27));
        rollErrorTxt->setReadOnly(true);
        rollEstimTxt = new QLineEdit(centralWidget);
        rollEstimTxt->setObjectName(QStringLiteral("rollEstimTxt"));
        rollEstimTxt->setEnabled(false);
        rollEstimTxt->setGeometry(QRect(270, 480, 51, 27));
        rollEstimTxt->setReadOnly(true);
        lineEdit_14 = new QLineEdit(centralWidget);
        lineEdit_14->setObjectName(QStringLiteral("lineEdit_14"));
        lineEdit_14->setGeometry(QRect(270, 450, 51, 27));
        zErrorTxt = new QLineEdit(centralWidget);
        zErrorTxt->setObjectName(QStringLiteral("zErrorTxt"));
        zErrorTxt->setEnabled(false);
        zErrorTxt->setGeometry(QRect(210, 510, 51, 27));
        zErrorTxt->setReadOnly(true);
        yawEstimTxt = new QLineEdit(centralWidget);
        yawEstimTxt->setObjectName(QStringLiteral("yawEstimTxt"));
        yawEstimTxt->setEnabled(false);
        yawEstimTxt->setGeometry(QRect(390, 480, 51, 27));
        yawEstimTxt->setReadOnly(true);
        yawErrorTxt = new QLineEdit(centralWidget);
        yawErrorTxt->setObjectName(QStringLiteral("yawErrorTxt"));
        yawErrorTxt->setEnabled(false);
        yawErrorTxt->setGeometry(QRect(390, 510, 51, 27));
        yawErrorTxt->setReadOnly(true);
        yawRealTxt = new QLineEdit(centralWidget);
        yawRealTxt->setObjectName(QStringLiteral("yawRealTxt"));
        yawRealTxt->setGeometry(QRect(390, 450, 51, 27));
        label_4 = new QLabel(centralWidget);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(100, 550, 41, 17));
        label_5 = new QLabel(centralWidget);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(270, 550, 51, 17));
        radialErrorTxt = new QLineEdit(centralWidget);
        radialErrorTxt->setObjectName(QStringLiteral("radialErrorTxt"));
        radialErrorTxt->setEnabled(false);
        radialErrorTxt->setGeometry(QRect(150, 540, 111, 27));
        radialErrorTxt->setReadOnly(true);
        angularErrorTxt = new QLineEdit(centralWidget);
        angularErrorTxt->setObjectName(QStringLiteral("angularErrorTxt"));
        angularErrorTxt->setEnabled(false);
        angularErrorTxt->setGeometry(QRect(330, 540, 111, 27));
        angularErrorTxt->setReadOnly(true);
        pitchRealTxt = new QLineEdit(centralWidget);
        pitchRealTxt->setObjectName(QStringLiteral("pitchRealTxt"));
        pitchRealTxt->setGeometry(QRect(330, 450, 51, 27));
        xRealTxt = new QLineEdit(centralWidget);
        xRealTxt->setObjectName(QStringLiteral("xRealTxt"));
        xRealTxt->setGeometry(QRect(90, 450, 51, 27));
        yRealTxt = new QLineEdit(centralWidget);
        yRealTxt->setObjectName(QStringLiteral("yRealTxt"));
        yRealTxt->setGeometry(QRect(150, 450, 51, 27));
        zRealTxt = new QLineEdit(centralWidget);
        zRealTxt->setObjectName(QStringLiteral("zRealTxt"));
        zRealTxt->setGeometry(QRect(210, 450, 51, 27));
        rollRealTxt = new QLineEdit(centralWidget);
        rollRealTxt->setObjectName(QStringLiteral("rollRealTxt"));
        rollRealTxt->setGeometry(QRect(270, 450, 51, 27));
        realMarkerChk = new QCheckBox(centralWidget);
        realMarkerChk->setObjectName(QStringLiteral("realMarkerChk"));
        realMarkerChk->setGeometry(QRect(320, 670, 181, 22));
        realMarkerChk->setTristate(false);
        arDemoChk = new QCheckBox(centralWidget);
        arDemoChk->setObjectName(QStringLiteral("arDemoChk"));
        arDemoChk->setGeometry(QRect(320, 700, 181, 22));
        arDemoChk->setTristate(false);
        corner0Txt = new QLineEdit(centralWidget);
        corner0Txt->setObjectName(QStringLiteral("corner0Txt"));
        corner0Txt->setEnabled(false);
        corner0Txt->setGeometry(QRect(230, 380, 51, 27));
        corner0Txt->setReadOnly(true);
        corner2Txt = new QLineEdit(centralWidget);
        corner2Txt->setObjectName(QStringLiteral("corner2Txt"));
        corner2Txt->setEnabled(false);
        corner2Txt->setGeometry(QRect(350, 380, 51, 27));
        corner2Txt->setReadOnly(true);
        corner1Txt = new QLineEdit(centralWidget);
        corner1Txt->setObjectName(QStringLiteral("corner1Txt"));
        corner1Txt->setEnabled(false);
        corner1Txt->setGeometry(QRect(290, 380, 51, 27));
        corner1Txt->setReadOnly(true);
        corner3Txt = new QLineEdit(centralWidget);
        corner3Txt->setObjectName(QStringLiteral("corner3Txt"));
        corner3Txt->setEnabled(false);
        corner3Txt->setGeometry(QRect(410, 380, 51, 27));
        corner3Txt->setReadOnly(true);
        label_6 = new QLabel(centralWidget);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(10, 390, 161, 17));
        markerIdTxt = new QLineEdit(centralWidget);
        markerIdTxt->setObjectName(QStringLiteral("markerIdTxt"));
        markerIdTxt->setGeometry(QRect(170, 380, 51, 27));
        copyBtn = new QPushButton(centralWidget);
        copyBtn->setObjectName(QStringLiteral("copyBtn"));
        copyBtn->setGeometry(QRect(450, 480, 61, 27));
        plusBtn = new QPushButton(centralWidget);
        plusBtn->setObjectName(QStringLiteral("plusBtn"));
        plusBtn->setGeometry(QRect(480, 450, 31, 27));
        minusBtn = new QPushButton(centralWidget);
        minusBtn->setObjectName(QStringLiteral("minusBtn"));
        minusBtn->setGeometry(QRect(450, 450, 31, 27));
        tempFusionGrp_2 = new QGroupBox(centralWidget);
        tempFusionGrp_2->setObjectName(QStringLiteral("tempFusionGrp_2"));
        tempFusionGrp_2->setGeometry(QRect(90, 410, 381, 21));
        xRdb = new QRadioButton(tempFusionGrp_2);
        xRdb->setObjectName(QStringLiteral("xRdb"));
        xRdb->setEnabled(true);
        xRdb->setGeometry(QRect(20, 0, 21, 21));
        xRdb->setChecked(false);
        yRdb = new QRadioButton(tempFusionGrp_2);
        yRdb->setObjectName(QStringLiteral("yRdb"));
        yRdb->setEnabled(true);
        yRdb->setGeometry(QRect(80, 0, 21, 21));
        zRdb = new QRadioButton(tempFusionGrp_2);
        zRdb->setObjectName(QStringLiteral("zRdb"));
        zRdb->setEnabled(true);
        zRdb->setGeometry(QRect(140, 0, 21, 21));
        rollRdb = new QRadioButton(tempFusionGrp_2);
        rollRdb->setObjectName(QStringLiteral("rollRdb"));
        rollRdb->setEnabled(true);
        rollRdb->setGeometry(QRect(200, 0, 21, 21));
        pitchRdb = new QRadioButton(tempFusionGrp_2);
        pitchRdb->setObjectName(QStringLiteral("pitchRdb"));
        pitchRdb->setEnabled(true);
        pitchRdb->setGeometry(QRect(260, 0, 21, 21));
        yawRdb = new QRadioButton(tempFusionGrp_2);
        yawRdb->setObjectName(QStringLiteral("yawRdb"));
        yawRdb->setEnabled(true);
        yawRdb->setGeometry(QRect(320, 0, 21, 21));
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 520, 19));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0));
        worldBtn->setText(QApplication::translate("MainWindow", "Show World", 0));
        cameraLbl->setText(QString());
        tempFusionGrp->setTitle(QApplication::translate("MainWindow", "Temporal Fusion", 0));
        kalmanRdb->setText(QApplication::translate("MainWindow", "Kalman", 0));
        tempFusionChk->setText(QString());
        weightRdb->setText(QApplication::translate("MainWindow", "Weighted Average", 0));
        errorBtn->setText(QApplication::translate("MainWindow", "Register", 0));
        label->setText(QApplication::translate("MainWindow", "Estimated", 0));
        label_9->setText(QApplication::translate("MainWindow", "Z", 0));
        label_10->setText(QApplication::translate("MainWindow", "Roll", 0));
        label_11->setText(QApplication::translate("MainWindow", "Pitch", 0));
        label_12->setText(QApplication::translate("MainWindow", "Yaw", 0));
        label_13->setText(QApplication::translate("MainWindow", "X", 0));
        label_2->setText(QApplication::translate("MainWindow", "Real", 0));
        label_14->setText(QApplication::translate("MainWindow", "Y", 0));
        label_3->setText(QApplication::translate("MainWindow", "Error", 0));
        lineEdit->setText(QString());
        xEstimTxt->setText(QString());
        xErrorTxt->setText(QString());
        lineEdit_4->setText(QString());
        yEstimTxt->setText(QString());
        yErrorTxt->setText(QString());
        lineEdit_7->setText(QString());
        zEstimTxt->setText(QString());
        pitchErrorTxt->setText(QString());
        pitchEstimTxt->setText(QString());
        lineEdit_11->setText(QString());
        rollErrorTxt->setText(QString());
        rollEstimTxt->setText(QString());
        lineEdit_14->setText(QString());
        zErrorTxt->setText(QString());
        yawEstimTxt->setText(QString());
        yawErrorTxt->setText(QString());
        yawRealTxt->setText(QApplication::translate("MainWindow", "0", 0));
        label_4->setText(QApplication::translate("MainWindow", "Radial", 0));
        label_5->setText(QApplication::translate("MainWindow", "Angular", 0));
        radialErrorTxt->setText(QString());
        angularErrorTxt->setText(QString());
        pitchRealTxt->setText(QApplication::translate("MainWindow", "0", 0));
        xRealTxt->setText(QApplication::translate("MainWindow", "0", 0));
        yRealTxt->setText(QApplication::translate("MainWindow", "0", 0));
        zRealTxt->setText(QApplication::translate("MainWindow", "0", 0));
        rollRealTxt->setText(QApplication::translate("MainWindow", "0", 0));
        realMarkerChk->setText(QApplication::translate("MainWindow", "Real marker projection", 0));
        arDemoChk->setText(QApplication::translate("MainWindow", "A. R. demo", 0));
        corner0Txt->setText(QString());
        corner2Txt->setText(QString());
        corner1Txt->setText(QString());
        corner3Txt->setText(QString());
        label_6->setText(QApplication::translate("MainWindow", "Marker detection error", 0));
        markerIdTxt->setText(QApplication::translate("MainWindow", "0", 0));
        copyBtn->setText(QApplication::translate("MainWindow", "Copy", 0));
        plusBtn->setText(QApplication::translate("MainWindow", "+", 0));
        minusBtn->setText(QApplication::translate("MainWindow", "-", 0));
        tempFusionGrp_2->setTitle(QString());
        xRdb->setText(QString());
        yRdb->setText(QString());
        zRdb->setText(QString());
        rollRdb->setText(QString());
        pitchRdb->setText(QString());
        yawRdb->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
