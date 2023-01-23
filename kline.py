# -*- coding:utf-8 -*-
#! python3

# FaceCat-Python-Wasm(OpenSource)
#Shanghai JuanJuanMao Information Technology Co., Ltd 

import win32gui
import win32api
from win32con import *
from xml.etree import ElementTree as ET
import math
import requests
import time
from requests.adapters import HTTPAdapter
from facecat import *
import facecat
import datetime
import os
from ctypes import *

#更新悬浮状态
#views:视图集合
def updateView(views):
	for i in range(0,len(views)):
		view = views[i]
		if(view.m_dock == "fill"):
			if(view.m_parent != None and view.m_parent.m_type != "split"):
				view.m_location = FCPoint(0, 0)
				view.m_size = FCSize(view.m_parent.m_size.cx, view.m_parent.m_size.cy)
		if(view.m_type == "split"):
			resetSplitLayoutDiv(view)
		elif(view.m_type == "tabview"):
			updateTabLayout(view)
		elif(view.m_type == "layout"):
			resetLayoutDiv(view)
		subViews = view.m_views
		if(len(subViews) > 0):
			updateView(subViews)

#设置属性
#view:视图
#node:xml节点
def setAttribute(view, child):
	if(view.m_paint != None):
		if(view.m_paint.m_defaultUIStyle == "dark"):
			view.m_backColor = "rgb(0,0,0)"
			view.m_borderColor = "rgb(100,100,100)"
			view.m_textColor = "rgb(255,255,255)"
		elif(view.m_paint.m_defaultUIStyle == "light"):
			view.m_backColor = "rgb(255,255,255)"
			view.m_borderColor = "rgb(150,150,150)"
			view.m_textColor = "rgb(0,0,0)"
		for key in child.attrib:
			name = key.lower()
			value = child.attrib[key]
			if(name == "location"):
				view.m_location = FCPoint(int(value.split(',')[0]), int(value.split(',')[1]))
			elif(name == "size"):
				view.m_size = FCSize(int(value.split(',')[0]), int(value.split(',')[1]))
			elif(name == "text"):
				view.m_text = value
			elif(name == "backcolor"):
				lowerStr = value.lower()
				if(lowerStr.find("rgb") == 0):
					view.m_backColor = value
				else:
					view.m_backColor = "none"
			elif(name == "bordercolor"):
				lowerStr = value.lower()
				if(lowerStr.find("rgb") == 0):
					view.m_borderColor = value
				else:
					view.m_borderColor = "none"
			elif(name == "textcolor"):
				lowerStr = value.lower()
				if(lowerStr.find("rgb") == 0):
					view.m_textColor = value
				else:
					view.m_textColor = "none"
			elif(name == "layoutstyle"):
				view.m_layoutStyle = value.lower()
			elif(name == "dock"):
				view.m_dock = value;
			elif(name == "font"):
				family = value.split(',')[0]
				if(family == "Default"):
					family = "Arial"
				view.m_font = value.split(',')[1] + "px " + family
			elif(name == "headerheight"):
				view.m_headerHeight = float(value)
			elif(name == "splitmode"):
				view.m_splitMode = value.lower()
			elif(name == "autowrap"):
				view.m_autoWrap = (value.lower() == "true")
			elif(name == "name"):
				view.m_name = value;
			elif(name == "showvscrollbar"):
				view.m_showVScrollBar = (value.lower() == "true")
			elif(name == "showhscrollbar"):
				view.m_showHScrollBar = (value.lower() == "true")
			elif(name == "visible"):
				view.m_visible =  (value.lower() == "true")
			elif(name == "displayoffset"):
				view.m_visible =  (value.lower() == "true")
			elif(name == "checked"):
				view.m_checked =  (value.lower() == "true")
			elif(name == "buttonsize"):
				view.m_buttonSize = FCSize(int(value.split(',')[0]), int(value.split(',')[1]))
			elif(name == "topmost"):
				view.m_topMost =  (value.lower() == "true")
			elif(name == "selectedindex"):
				view.m_selectedIndex = int(value)
			elif(name == "src"):
				view.m_src = value
			elif(name == "backimage"):
				view.m_backImage = value
			elif(name == "allowdrag"):
				view.m_allowDrag =  (value.lower() == "true")
    
#读取Xml
#paint 绘图对象
#node节点
#parent 父视图
def readXmlNode(paint, node, parent):
	for child in node:
		view = None
		typeStr = ""
		nodeName = child.tag.replace("{facecat}", "").lower()
		if(nodeName == "div" or nodeName == "view"):
			if "type" in child.attrib:
				typeStr = child.attrib["type"]
			if(typeStr == "splitlayout"):
				view = FCSplitLayoutDiv()
			elif(typeStr == "layout"):
				view = FCLayoutDiv()
			elif(typeStr == "tab"):
				view = FCTabView()
			elif(typeStr == "tabpage"):
				view = FCTabPage()
			elif(typeStr == "radio"):
				view = FCRadioButton()
				view.m_backColor = "none"
			elif(typeStr == "checkbox"):
				view = FCCheckBox()
				view.m_backColor = "none"
			elif(typeStr == "button"):
				view = FCView()
				view.m_type = "button"
			elif(typeStr == "text" or typeStr == "range" or typeStr == "datetime"):
				view = FCView()
				view.m_type = "textbox"
			else:
				view = FCView()
				view.m_type = "div"
		elif(nodeName == "table"):
			view = FCGrid()
		elif(nodeName == "chart"):
			view = FCChart()
		elif(nodeName == "tree"):
			view = FCTree()
		elif(nodeName == "select"):
			view = FCView()
			view.m_type = "combobox"
		elif(nodeName == "input" ):
			if "type" in child.attrib:
				typeStr = child.attrib["type"]
			if(typeStr == "radio"):
				view = FCRadioButton()
				view.m_backColor = "none"
			elif(typeStr == "checkbox"):
				view = FCCheckBox()
				view.m_backColor = "none"
			elif(typeStr == "button"):
				view = FCView()
				view.m_type = "button"
			elif(typeStr == "text" or typeStr == "range" or typeStr == "datetime"):
				view = FCView()
				view.m_type = "textbox"
			else:
				view = FCView()
				view.m_type = "button"
		else:
			view = FCView()
		view.m_paint = paint
		view.m_parent = parent
		setAttribute(view, child)
		if(nodeName == "label"):
			view.m_type = "label"
			view.m_borderColor = "none"
		if(view != None):
			if(typeStr == "tabpage"):
				tabButton = FCView()
				tabButton.m_type = "tabbutton"
				if "headersize" in child.attrib:
					atrHeaderSize = child.attrib["headersize"]
					tabButton.m_size = FCSize(int(atrHeaderSize.split(',')[0]), int(atrHeaderSize.split(',')[1]))
				else:
					tabButton.m_size = FCSize(100, 20)
				if(view.m_paint.m_defaultUIStyle == "dark"):
					tabButton.m_backColor = "rgb(0,0,0)"
					tabButton.m_borderColor = "rgb(100,100,100)"
					tabButton.m_textColor = "rgb(255,255,255)"
				elif(view.m_paint.m_defaultUIStyle == "light"):
					tabButton.m_backColor = "rgb(255,255,255)"
					tabButton.m_borderColor = "rgb(150,150,150)"
					tabButton.m_textColor = "rgb(0,0,0)"
				tabButton.m_text = view.m_text
				tabButton.m_paint = paint
				addTabPage(view.m_parent, view, tabButton)
			else:
				if(parent != None):
					parent.m_views.append(view)
				else:
					paint.m_views.append(view)
			if(typeStr == "splitlayout"):
				if "datumsize" in child.attrib:
					atrDatum = child.attrib["datumsize"]
					view.m_size = FCSize(int(atrDatum.split(',')[0]), int(atrDatum.split(',')[1]))
				splitter = FCView()
				splitter.m_paint = paint
				splitter.m_parent = view
				if(view.m_paint.m_defaultUIStyle == "dark"):
					splitter.m_backColor = "rgb(100,100,100)"
				elif(view.m_paint.m_defaultUIStyle == "light"):
					splitter.m_backColor = "rgb(150,150,150)"
				if "candragsplitter" in child.attrib:
					if(child.attrib["candragsplitter"] == "true"):
						splitter.m_allowDrag = TRUE
				view.m_splitter = splitter
				splitterposition = child.attrib["splitterposition"]
				splitStr = splitterposition.split(',')
				if(len(splitStr) >= 4):
					splitRect = FCRect(float(splitStr[0]), float(splitStr[1]), float(splitStr[2]), float(splitStr[3]))
					splitter.m_location = FCPoint(splitRect.left, splitRect.top)
					splitter.m_size = FCSize(splitRect.right - splitRect.left, splitRect.bottom - splitRect.top)
				else:
					sSize = float(splitStr[1])
					sPosition = float(splitStr[0])
					if(view.m_layoutStyle == "lefttoright" or view.m_layoutStyle == "righttoleft"):
						splitter.m_location = FCPoint(sPosition, 0)
						splitter.m_size = FCSize(sSize, view.m_size.cy)
					else:
						splitter.m_location = FCPoint(0, sPosition)
						splitter.m_size = FCSize(view.m_size.cx, sSize)
				readXmlNode(paint, child, view)
				subViews = view.m_views
				view.m_firstView = subViews[0];
				view.m_secondView = subViews[1];
				view.m_views.append(splitter)
				view.m_oldSize = FCSize(view.m_size.cx, view.m_size.cy)
				resetSplitLayoutDiv(view)
			elif(typeStr == "tab"):
				readXmlNode(paint, child, view)
				tabPages = view.m_tabPages
				if(len(tabPages) > 0):
					tabPages[0].m_visible = TRUE
			elif(nodeName == "table"):
				for tChild in child:
					if(tChild.tag.replace("{facecat}", "") == "tr"):
						for sunNode in tChild:
							sunNodeName = sunNode.tag.lower().replace("{facecat}", "")
							if(sunNodeName == "th"):
								gridColumn = FCGridColumn()
								gridColumn.m_width = 100
								if "text" in  sunNode.attrib:
									gridColumn.m_text = sunNode.attrib["text"]
								view.m_columns.append(gridColumn)
								if(view.m_paint.m_defaultUIStyle == "light"):
									gridColumn.m_backColor = "rgb(230,230,230)"
									gridColumn.m_borderColor = "rgb(150,150,150)"
									gridColumn.m_textColor = "rgb(0,0,0)"
			elif(view.m_type == "textbox"):
				if(paint.m_useGdiPlus and len(view.m_name) > 0):
					paint.init()
					paint.m_gdiPlusPaint.createView("textbox", view.m_name)
					if(view.m_paint.m_defaultUIStyle == "dark"):
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "backcolor", "rgb(0,0,0)")
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "bordercolor", "rgb(100,100,100)")
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "textcolor", "rgb(255,255,255)")
					elif(view.m_paint.m_defaultUIStyle == "light"):
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "backcolor", "rgb(255,255,255)")
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "bordercolor", "rgb(150,150,150)")
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "textcolor", "rgb(0,0,0)")
					for key in child.attrib:
						name = key.lower()
						value = child.attrib[key]
						paint.m_gdiPlusPaint.setAttribute(view.m_name, name, value)
				else:
					view.m_hWnd = win32gui.CreateWindowEx(0, "Edit", view.m_name, WS_VISIBLE|WS_CHILD|SS_CENTERIMAGE, 0, 0, 100, 30, paint.m_hWnd, 0, 0, None)
					win32gui.ShowWindow(view.m_hWnd, SW_HIDE)
					s = win32gui.GetWindowLong(view.m_hWnd, GWL_EXSTYLE)
					win32gui.SetWindowLong(view.m_hWnd, GWL_EXSTYLE, s|ES_CENTER)
					setHWndText(view.m_hWnd, view.m_text)
			elif(view.m_type == "combobox"):
				#https://blog.csdn.net/qq_31178679/article/details/125883494
				view.m_hWnd = win32gui.CreateWindowEx(0, "ComboBox", view.m_name, WS_VISIBLE | WS_CHILD | WS_BORDER | CBS_HASSTRINGS | CBS_DROPDOWNLIST, 0, 0, 100, 30, paint.m_hWnd, 0, 0, None)
				win32gui.ShowWindow(view.m_hWnd, SW_HIDE)
				cIndex = 0
				for tChild in child:
					if(tChild.tag.replace("{facecat}", "") == "option"):
						if "text" in tChild.attrib:
							win32gui.SendMessage(view.m_hWnd, CB_ADDSTRING, cIndex, tChild.attrib["text"])
							cIndex = cIndex + 1
				if "selectedindex" in child.attrib:
					win32gui.SendMessage(view.m_hWnd, CB_SETCURSEL, int(child.attrib["selectedindex"]), 0)
			else:
				readXmlNode(paint, child, view)

#绘制视图
#view:视图
#paint:绘图对象
#clipRect:区域
def onViewPaint(view, paint, clipRect):
	if(view.m_type == "radiobutton"):
		drawRadioButton(view, paint, clipRect)
	elif(view.m_type == "checkbox"):
		drawCheckBox(view, paint, clipRect)
	elif(view.m_type == "chart"):
		resetChartVisibleRecord(view)
		checkChartLastVisibleIndex(view)
		calculateChartMaxMin(view)
		drawChart(view, paint, clipRect)
		global m_currentFormula
		strs = m_currentFormula.split("\n")
		pos = 0
		for i in range(0, len(strs)):
			if(len(strs[i]) > 1):
				paint.drawText(strs[i], view.m_textColor, "14px Arial", 0, pos * 25)
				pos = pos + 1		
	elif(view.m_type == "grid"):
		drawDiv(view, paint, clipRect)
		drawGrid(view, paint, clipRect)
	elif(view.m_type == "tree"):
		drawDiv(view, paint, clipRect)
		drawTree(view, paint, clipRect)
	elif(view.m_type == "label"):
		if(view.m_textColor != "none"):
			tSize = paint.textSize(view.m_text, view.m_font)
			paint.drawText(view.m_text, view.m_textColor, view.m_font, 0, (view.m_size.cy - tSize.cy) / 2)
	elif(view.m_type == "div" or view.m_type =="tabpage" or view.m_type =="tabview" or view.m_type =="layout"):
		drawDiv(view, paint, clipRect)
	elif(view.m_type == "textbox"):
		if(paint.m_gdiPlusPaint.m_useGdiPlus):
			paint.m_gdiPlusPaint.paintView(view.m_name, 0, 0, view.m_size.cx, view.m_size.cy)
	else:
		drawButton(view, paint, clipRect)

#绘制视图边线
#view:视图
#paint:绘图对象
#clipRect:区域
def onViewPaintBorder(view, paint, clipRect):
	if(view.m_type == "grid"):
		drawGridScrollBar(view, paint, clipRect)
	elif(view.m_type == "tree"):
		drawTreeScrollBar(view, paint, clipRect)
	elif(view.m_type == "div" or view.m_type =="tabpage" or view.m_type =="tabview" or view.m_type =="layout"):
		drawDivScrollBar(view, paint, clipRect)
		drawDivBorder(view, paint, clipRect)

#视图的鼠标移动方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseMove(view, mp, buttons, clicks, delta):
	firstTouch = FALSE
	secondTouch = FALSE
	firstPoint = mp
	secondPoint = mp
	if (buttons == 1):
		firstTouch = TRUE
	if (view.m_type == "grid"):
		mouseMoveGrid(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "tree"):
		mouseMoveTree(view, firstTouch, secondTouch, firstPoint, secondPoint)
	elif(view.m_type == "chart"):
		mouseMoveChart(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "div" or view.m_type =="layout"):
		mouseMoveDiv(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "button"):
		invalidateView(view, view.m_paint)
		
#视图的鼠标按下方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseDown(view, mp, buttons, clicks, delta):
	global m_addingPlot_Chart
	firstTouch = FALSE
	secondTouch = FALSE
	firstPoint = mp
	secondPoint = mp
	if (buttons == 1):
		firstTouch = TRUE
	if (view.m_type == "grid"):
		mouseDownGrid(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "tree"):
		mouseDownTree(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "chart"):
		view.m_selectShape = ""
		view.m_selectShapeEx = ""
		facecat.m_mouseDownPoint_Chart = mp;
		if(len(m_addingPlot_Chart) > 0):
			if (mp.y < getCandleDivHeight(view)):
				touchIndex = getChartIndex(view, mp)
				if (touchIndex >= view.m_firstVisibleIndex and touchIndex <= view.m_lastVisibleIndex):
					if(m_addingPlot_Chart == "FiboTimezone"):
						fIndex = touchIndex
						fDate = getChartDateByIndex(view, fIndex)
						y = getCandleDivValue(view, mp)
						newPlot = FCPlot()
						if(view.m_paint.m_defaultUIStyle == "light"):
							newPlot.m_lineColor = "rgb(0,0,0)"
							newPlot.m_pointColor = "rgba(0,0,0,0.5)"
						newPlot.m_key1 = fDate
						newPlot.m_value1 = y
						newPlot.m_plotType = m_addingPlot_Chart
						view.m_plots.append(newPlot)
						view.m_sPlot = selectPlot(view, mp)
					elif (m_addingPlot_Chart == "Triangle" or m_addingPlot_Chart == "CircumCycle" or m_addingPlot_Chart == "ParalleGram" or m_addingPlot_Chart == "AngleLine" or m_addingPlot_Chart == "Parallel" or m_addingPlot_Chart == "SymmetricTriangle"):
						eIndex = touchIndex;
						bIndex = eIndex - 5;
						if (bIndex >= 0):
							fDate = getChartDateByIndex(view, bIndex)
							sDate = getChartDateByIndex(view, eIndex)
							y = getCandleDivValue(view, mp)
							newPlot = FCPlot()
							if(view.m_paint.m_defaultUIStyle == "light"):
								newPlot.m_lineColor = "rgb(0,0,0)"
								newPlot.m_pointColor = "rgba(0,0,0,0.5)"
							newPlot.m_key1 = fDate
							newPlot.m_value1 = y
							newPlot.m_key2 = sDate
							newPlot.m_value2 = y
							newPlot.m_key3 = sDate
							newPlot.m_value3 = view.m_candleMin + (view.m_candleMax - view.m_candleMin) / 2
							newPlot.m_plotType = m_addingPlot_Chart
							view.m_plots.append(newPlot)
							view.m_sPlot = selectPlot(view, mp)
					else:
						eIndex = touchIndex
						bIndex = eIndex - 5
						if (bIndex >= 0):
							fDate = getChartDateByIndex(view, bIndex)
							sDate = getChartDateByIndex(view, eIndex)
							y = getCandleDivValue(view, mp)
							newPlot = FCPlot()
							if(view.m_paint.m_defaultUIStyle == "light"):
								newPlot.m_lineColor = "rgb(0,0,0)"
								newPlot.m_pointColor = "rgba(0,0,0,0.5)"
							newPlot.m_key1 = fDate
							newPlot.m_value1 = y
							newPlot.m_key2 = sDate
							newPlot.m_value2 = y
							newPlot.m_plotType = m_addingPlot_Chart
							view.m_plots.append(newPlot)
							view.m_sPlot = selectPlot(view, mp)
			m_addingPlot_Chart = ""
		view.m_sPlot = selectPlot(view, mp)
		if (view.m_sPlot == None):
			selectShape(view, mp)
	elif(view.m_type == "div" or view.m_type =="layout"):
		mouseDownDiv(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "button"):
		invalidateView(view, view.m_paint)

#视图的鼠标抬起方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseUp(view, mp, buttons, clicks, delta):
	firstTouch = FALSE
	secondTouch = FALSE
	firstPoint = mp
	secondPoint = mp
	if (buttons == 1):
		firstTouch = TRUE
	if (view.m_type == "grid"):
		mouseUpGrid(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "tree"):
		mouseUpTree(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "div" or view.m_type =="layout"):
		mouseUpDiv(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "chart"):
		facecat.m_firstTouchIndexCache_Chart = -1
		facecat.m_secondTouchIndexCache_Chart = -1
		invalidateView(view, view.m_paint)
	elif(view.m_type == "button"):
		invalidateView(view, view.m_paint)

m_addingPlot_Chart = ""

#视图的鼠标点击方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewClick(view, mp, buttons, clicks, delta):
	global m_addingPlot_Chart
	global m_drawColors
	if(view.m_type == "radiobutton"):
		clickRadioButton(view, mp)
		if(view.m_parent != None):
			invalidateView(view.m_parent, view.m_parent.m_paint)
		else:
			invalidateView(view, view.m_paint)
	elif(view.m_type == "checkbox"):
		clickCheckBox(view, mp)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "tabbutton"):
		tabView = view.m_parent
		for i in range(0, len(tabView.m_tabPages)):
			if(tabView.m_tabPages[i].m_headerButton == view):
				selectTabPage(tabView, tabView.m_tabPages[i])
		invalidateView(tabView, tabView.m_paint)
	elif(view.m_type == "plot"):
		m_addingPlot_Chart = view.m_text
	elif(view.m_type == "indicator"):
		m_chart = findViewByName("chart", m_paint.m_views)
		if (view.m_text == "BOLL" or view.m_text == "MA"):
			m_chart.m_mainIndicator = view.m_text
		else:
			m_chart.m_showIndicator = view.m_text
		calcChartIndicator(m_chart)
		invalidateView(m_chart, m_chart.m_paint)
	elif(view.m_name == "formula"):
		bindFormula(view.m_text, TRUE, 2)
		

#绑定公式
def bindFormula(name, clearOld, divIndex):
	global m_shapes
	global m_currentFormula
	file0 = open(os.getcwd() + "\\" + name, encoding="UTF-8")
	formulaStr = file0.read()
	file0.close()
	m_currentFormula = formulaStr
	#计算指标
	m_chart = findViewByName("chart", m_paint.m_views)
	result = calculateFormulaWithShapes(formulaStr, m_chart.m_data)
	if(clearOld):
		m_chart.m_shapes = []
	shapesArray = m_shapes.split("\r\n")
	for s in range(0, len(shapesArray)):
		subStrs = shapesArray[s].split(",")
		if(len(subStrs) >= 2):
			if(subStrs[0] == "bar"):
				if(len(subStrs[1]) > 0):
					is2Color = FALSE
					if(len(subStrs) == 2 or len(subStrs[2]) == 0):
						is2Color = TRUE
					bar1 = BaseShape()
					s = s + 1
					colorStrs = shapesArray[s].split("|")
					bar1.m_color = colorStrs[0]
					bar1.m_color2 =  colorStrs[1]
					bar1.m_divIndex = divIndex
					bar1.m_type = "bar"
					bar1.m_name = subStrs[1]					
					if(is2Color):
						bar1.m_style = "2color"
						bar1.m_title = subStrs[1]
					else:
						s = s + 1
						bar1.m_showHideDatas = shapesArray[s].split(",")
					m_chart.m_shapes.append(bar1)
					resultStrs = result.split("\r\n")
					colIndex = 0
					colIndex2 = 1
					for r in range(0, len(resultStrs)):
						sunStrs = resultStrs[r].split(",")
						if(r == 0):
							for u in range(0, len(sunStrs)):
								if(sunStrs[u] == subStrs[1]):
									colIndex = u
								if(is2Color == FALSE):
									if(sunStrs[u] == subStrs[2]):
										colIndex2 = u
						else:
							if(len(sunStrs) >= colIndex + 1):
								if(len(sunStrs[colIndex]) > 0 and sunStrs[colIndex] != '1.#QNAN0'):
									bar1.m_datas.append(float(sunStrs[colIndex]))
								else:
									bar1.m_datas.append(0)
								if(is2Color == FALSE):
									if(len(sunStrs[colIndex2]) > 0 and sunStrs[colIndex2] != '1.#QNAN0'):
										bar1.m_datas2.append(float(sunStrs[colIndex2]))
									else:
										bar1.m_datas2.append(0)
	for s in range(0, len(shapesArray)):
		subStrs = shapesArray[s].split(",")
		if(len(subStrs) >= 2):
			if(subStrs[0] == "line"):
				line1 = BaseShape()
				s = s + 1
				line1.m_color = shapesArray[s]
				line1.m_divIndex = divIndex
				line1.m_name = subStrs[1]
				line1.m_title = subStrs[1]
				m_chart.m_shapes.append(line1)
				resultStrs = result.split("\r\n")
				colIndex = 0
				for r in range(0, len(resultStrs)):
					sunStrs = resultStrs[r].split(",")
					if(r == 0):
						for u in range(0, len(sunStrs)):
							if(sunStrs[u] == subStrs[1]):
								colIndex = u
								break
					else:
						if(len(sunStrs) >= colIndex + 1):
							if(len(sunStrs[colIndex]) > 0 and sunStrs[colIndex] != '1.#QNAN0'):
								line1.m_datas.append(float(sunStrs[colIndex]))
							else:
								line1.m_datas.append(0)
	for s in range(0, len(shapesArray)):
		subStrs = shapesArray[s].split(",")
		if(len(subStrs) >= 2):
			if(subStrs[0] == "text"):
				textShape = BaseShape()
				s = s + 1
				textShape.m_text = shapesArray[s]
				s = s + 1
				textShape.m_color = shapesArray[s]
				textShape.m_divIndex = divIndex
				textShape.m_type = "text"
				textShape.m_name = subStrs[1]
				textShape.m_title = subStrs[1]
				m_chart.m_shapes.append(textShape)
				resultStrs = result.split("\r\n")
				colIndex = 0
				for r in range(0, len(resultStrs)):
					sunStrs = resultStrs[r].split(",")
					if(r == 0):
						for u in range(0, len(sunStrs)):
							if(sunStrs[u] == subStrs[1]):
								colIndex = u
								break
					else:
						if(len(sunStrs) >= colIndex + 1):
							if(len(sunStrs[colIndex]) > 0 and sunStrs[colIndex] != '1.#QNAN0'):
								textShape.m_value = float(sunStrs[colIndex])
								textShape.m_datas.append(1)
							else:
								textShape.m_datas.append(0)
	calcChartIndicator(m_chart)
	invalidateView(m_chart, m_chart.m_paint)
	

#视图的鼠标滚动方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseWheel(view, mp, buttons, clicks, delta):
	if (view.m_type == "grid"):
		mouseWheelGrid(view, delta)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "tree"):
		mouseWheelTree(view, delta)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "div" or view.m_type =="layout"):
		mouseWheelDiv(view, delta)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "chart"):
		if(delta > 0):
			zoomOutChart(view);
		elif(delta < 0):
			zoomInChart(view);
		invalidateView(view, view.m_paint)

facecatcpp = cdll.LoadLibrary(os.getcwd() + r"\\facecatcpp.dll")
cdll.argtypes = [c_char_p, c_int, c_double, c_long, c_wchar_p]

#K线数据转字符串
#datas 数据
def securityDatasToStr(datas):
	result = ""
	for i in range(0, len(datas)):
		data = datas[i]
		result = result + str(data.m_date) + "," + str(data.m_close) + "," + str(data.m_high) + "," + str(data.m_low) + "," + str(data.m_open) + "," + str(data.m_volume) + "\r"
	return result

#调用C++计算指标
#formula 公式
#datas 数据
def calculateFormula(formula, datas):
	recvData = create_string_buffer(1024 * 1024 * 10)
	sendStr = securityDatasToStr(datas)
	facecatcpp.calcFormula(c_char_p(formula.encode('gbk')), c_char_p(sendStr.encode('gbk')), recvData)
	return str(recvData.value, encoding="gbk")

m_shapes = ""
m_currentFormula = ""
#调用C++计算指标，附带图形返回
#formula 公式
#datas 数据
def calculateFormulaWithShapes(formula, datas):
	global m_shapes
	recvData = create_string_buffer(1024 * 1024 * 10)
	recvData2 = create_string_buffer(1024 * 1024)
	sendStr = securityDatasToStr(datas)
	facecatcpp.calcFormulaWithShapes(c_char_p(formula.encode('gbk')), c_char_p(sendStr.encode('gbk')), recvData, recvData2)
	m_shapes = str(recvData2.value, encoding="gbk")
	return str(recvData.value, encoding="gbk")

#初始化K线
def initChart():
	global m_paint
	m_chart = findViewByName("chart", m_paint.m_views)
	m_layout = findViewByName("divLayout", m_paint.m_views)
	m_myLayout =  findViewByName("mylayout", m_paint.m_views)
	m_myLayout.m_showVScrollBar = TRUE
	m_myLayout.m_borderColor = "none"
	m_chart.m_leftVScaleWidth = 80
	m_chart.m_textColor = "rgb(255,255,255)"
	m_chart.m_mainIndicator = "MA"
	m_layout.m_showHScrollBar = TRUE
	m_layout.m_showVScrollBar = TRUE
	m_layout.m_allowDragScroll = TRUE
	m_layout.m_scrollSize = 0
	plots = []
	plots.append("Line")
	plots.append("Segment")
	plots.append("Ray")
	plots.append("Triangle")
	plots.append("Rect")
	plots.append("Cycle")
	plots.append("CircumCycle")
	plots.append("Ellipse")
	plots.append("AngleLine")
	plots.append("ParalleGram")
	plots.append("SpeedResist")
	plots.append("FiboFanline")
	plots.append("FiboTimezone")
	plots.append("Percent")
	plots.append("BoxLine")
	plots.append("TironeLevels")
	plots.append("Parallel")
	plots.append("GoldenRatio")
	plots.append("LRLine")
	plots.append("LRChannel")
	plots.append("LRBand")
	for i in range(0, len(plots)):
		subView = FCView()
		subView.m_type = "plot"
		subView.m_text = plots[i]
		subView.m_name = plots[i]
		subView.m_location = FCPoint(i * 100 + 1, 1)
		subView.m_size = FCSize(98, 28)
		addViewToParent(subView, m_layout)
		subView.m_allowDrag = TRUE
		if(subView.m_paint.m_defaultUIStyle == "dark"):
			subView.m_backColor = "rgb(0,0,0)"
			subView.m_borderColor = "rgb(100,100,100)"
			subView.m_textColor = "rgb(255,255,255)"
		elif(subView.m_paint.m_defaultUIStyle == "light"):
			subView.m_backColor = "rgb(255,255,255)"
			subView.m_borderColor = "rgb(150,150,150)"
			subView.m_textColor = "rgb(0,0,0)"
	indicators = []
	indicators.append("MA")
	indicators.append("BOLL")
	indicators.append("MACD")
	indicators.append("KDJ")
	indicators.append("BIAS")
	indicators.append("ROC")
	indicators.append("WR")
	indicators.append("DMA")
	indicators.append("RSI")
	indicators.append("BBI")
	indicators.append("CCI")
	indicators.append("TRIX")
	for i in range(0, len(indicators)):
		subView = FCView()
		subView.m_type = "indicator"
		subView.m_text = indicators[i]
		subView.m_name = indicators[i]
		subView.m_location = FCPoint(i * 100 + 1, 30)
		subView.m_size = FCSize(98, 28)
		addViewToParent(subView, m_layout)
		subView.m_allowDrag = TRUE
		m_layout.m_views.append(subView)
		if(subView.m_paint.m_defaultUIStyle == "dark"):
			subView.m_backColor = "rgb(0,0,0)"
			subView.m_borderColor = "rgb(100,100,100)"
			subView.m_textColor = "rgb(255,255,255)"
		elif(subView.m_paint.m_defaultUIStyle == "light"):
			subView.m_backColor = "rgb(255,255,255)"
			subView.m_borderColor = "rgb(150,150,150)"
			subView.m_textColor = "rgb(0,0,0)"
	file0 = open(os.getcwd() + "\\SH600000.txt", encoding="UTF-8")
	dataText = file0.read()
	file0.close()
	strs = dataText.split("\n")
	strLen = len(strs)
	for i in range(2, strLen - 1):
		subStrs = strs[i].split(",")
		if(len(subStrs) > 5):
			data = SecurityData()
			data.m_date = i
			data.m_close = float(subStrs[4])
			data.m_high = float(subStrs[2])
			data.m_low = float(subStrs[3])
			data.m_open = float(subStrs[1])
			data.m_volume = float(subStrs[6])
			m_chart.m_data.append(data)
	#testDiv4()
	calcChartIndicator(m_chart)
	files = os.listdir("./")
	for f in files:
		if(f.find(".js") != -1):
			indButton = FCView()
			indButton.m_type = "button"
			indButton.m_text = f
			indButton.m_name = "formula"
			indButton.m_size = FCSize(100, 40)
			addViewToParent(indButton, m_myLayout)
			if(indButton.m_paint.m_defaultUIStyle == "dark"):
				indButton.m_backColor = "rgb(0,0,0)"
				indButton.m_borderColor = "none"
				indButton.m_textColor = "rgb(255,255,255)"
			elif(indButton.m_paint.m_defaultUIStyle == "light"):
				indButton.m_backColor = "rgb(255,255,255)"
				indButton.m_borderColor = "none"
				indButton.m_textColor = "rgb(0,0,0)"			
	resetLayoutDiv(m_myLayout)
	bindFormula("指数平滑异同平均线(MACD).js", TRUE, 2)
	#m_chart.m_candleDivPercent = 0.45
	#m_chart.m_volDivPercent = 0.15
	#m_chart.m_indDivPercent = 0.2
	#m_chart.m_indDivPercent2 = 0.2
	#bindFormula("通达信火车轨(TDXHCG).js", FALSE, 2)
	#bindFormula("通达信明白K线(TDXMBKX).js", FALSE, 3)

m_xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<html xmlns=\"facecat\">\r\n  <head>\r\n  </head>\r\n  <body>\r\n    <div type=\"splitlayout\" layoutstyle=\"lefttoright\" bordercolor=\"none\" dock=\"fill\" size=\"400,400\" candragsplitter=\"true\" splitmode=\"AbsoluteSize\" splittervisible=\"true\" splitter-bordercolor=\"-200000000105\" splitterposition=\"250,5\">\r\n      <div type=\"layout\" name=\"mylayout\" layoutstyle=\"TopToBottom\">\r\n      </div>\r\n      <div type=\"splitlayout\" layoutstyle=\"bottomtotop\" bordercolor=\"none\" splitterposition=\"340,1\" dock=\"fill\" size=\"400,400\" candragsplitter=\"true\">\r\n        <div name=\"divLayout\" bordercolor=\"none\" />\r\n        <chart name=\"chart\" bordercolor=\"none\" />\r\n      </div>\r\n    </div>\r\n  </body>\r\n</html>"

m_paint = FCPaint() #创建绘图对象
facecat.m_paintCallBack = onViewPaint 
facecat.m_paintBorderCallBack = onViewPaintBorder 
facecat.m_mouseDownCallBack = onViewMouseDown 
facecat.m_mouseMoveCallBack = onViewMouseMove 
facecat.m_mouseUpCallBack = onViewMouseUp
facecat.m_mouseWheelCallBack = onViewMouseWheel
facecat.m_clickCallBack = onViewClick

def WndProc(hwnd,msg,wParam,lParam):
	if msg == WM_DESTROY:
		win32gui.PostQuitMessage(0)
	if(hwnd == m_paint.m_hWnd):
		if msg == WM_ERASEBKGND:
			return 1
		elif msg == WM_SIZE:
			rect = win32gui.GetClientRect(m_paint.m_hWnd)
			m_paint.m_size = FCSize(rect[2] - rect[0], rect[3] - rect[1])
			for view in m_paint.m_views:
				if view.m_dock == "fill":
					view.m_size = FCSize(m_paint.m_size.cx, m_paint.m_size.cy)
			updateView(m_paint.m_views)
			invalidate(m_paint)
		elif msg == WM_LBUTTONDOWN:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			onMouseDown(mp, 1, 1, 0, m_paint)
		elif msg == WM_LBUTTONDBLCLK:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			onMouseDown(mp, 1, 2, 0, m_paint)
		elif msg == WM_LBUTTONUP:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			onMouseUp(mp, 1, 1, 0, m_paint)
		elif msg == WM_MOUSEWHEEL:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			if(wParam > 4000000000):
				onMouseWheel(mp, 0, 0, -1, m_paint)
			else:
				onMouseWheel(mp, 0, 0, 1, m_paint)
		elif msg == WM_MOUSEMOVE:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			if(wParam == 1):
				onMouseMove(mp, 1, 1, 0, m_paint)
			elif(wParam == 2):
				onMouseMove(mp, 2, 1, 0, m_paint)
			else:
				onMouseMove(mp, 0, 0, 0, m_paint)
		elif msg == WM_PAINT:
			rect = win32gui.GetClientRect(m_paint.m_hWnd)
			m_paint.m_size = FCSize(rect[2] - rect[0], rect[3] - rect[1])
			for view in m_paint.m_views:
				if view.m_dock == "fill":
					view.m_size = FCSize(m_paint.m_size.cx, m_paint.m_size.cy)
			updateView(m_paint.m_views)
			invalidate(m_paint)
		elif msg == WM_IME_COMPOSITION or msg == WM_IME_CHAR or msg == WM_IME_SETCONTEXT:
			if(m_paint.m_useGdiPlus):
				m_paint.m_gdiPlusPaint.onMessage(hwnd,msg,wParam,lParam)
		elif msg == WM_CHAR or msg == WM_KEYDOWN or msg == WM_SYSKEYDOWN or msg == WM_KEYUP or msg == WM_SYSKEYUP:
			if(facecat.m_focusedView != None and facecat.m_focusedView.m_type == "textbox"):
				if(m_paint.m_useGdiPlus):
					m_paint.m_gdiPlusPaint.onMessage(hwnd,msg,wParam,lParam)
					invalidateView(facecat.m_focusedView, facecat.m_focusedView.m_paint)
	return win32gui.DefWindowProc(hwnd,msg,wParam,lParam)

wc = win32gui.WNDCLASS()
wc.hbrBackground = COLOR_BTNFACE + 1
wc.hCursor = win32gui.LoadCursor(0,IDI_APPLICATION)
wc.lpszClassName = "facecat-py"
wc.lpfnWndProc = WndProc
wc.style = CS_HREDRAW | CS_VREDRAW | CS_DBLCLKS
reg = win32gui.RegisterClass(wc)
hwnd = win32gui.CreateWindow(reg,'facecat-py',WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN,CW_USEDEFAULT,CW_USEDEFAULT,CW_USEDEFAULT,CW_USEDEFAULT,0,0,0,None)
m_paint.m_hWnd = hwnd
root = ET.fromstring(m_xml)
for child in root:
	if(child.tag == "{facecat}body"):
		readXmlNode(m_paint, child, None)
rect = win32gui.GetClientRect(hwnd)
m_paint.m_size = FCSize(rect[2] - rect[0], rect[3] - rect[1])
for view in m_paint.m_views:
	if view.m_dock == "fill":
		view.m_size = FCSize(m_paint.m_size.cx, m_paint.m_size.cy)
initChart()
updateView(m_paint.m_views)
win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)
win32gui.UpdateWindow(hwnd)
win32gui.PumpMessages()