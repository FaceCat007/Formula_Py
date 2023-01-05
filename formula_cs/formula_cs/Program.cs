using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;
using System.Net;
using System.IO;

namespace formula_cs
{
    class Program
    {
        /*
	    调用C++计算指标
	    formula 公式
	    recvData 接收数据
	    */
        [DllImport("facecatcpp.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public static extern int calcFormulaWithShapes(String formula, String sendStr, IntPtr recvData, IntPtr recvData2);
        public static int calcFormulaWithShapes(String formula, String sendStr, StringBuilder recvData, StringBuilder recvData2)
        {
            IntPtr bufferIntPtr = Marshal.AllocHGlobal(1024 * 1024 * 10);
            IntPtr bufferIntPtr2 = Marshal.AllocHGlobal(1024 * 1024);
            int state = calcFormulaWithShapes(formula, sendStr, bufferIntPtr, bufferIntPtr2);
            String sbResult = Marshal.PtrToStringAnsi(bufferIntPtr);
            recvData.Append(sbResult);
            String sbResult2 = Marshal.PtrToStringAnsi(bufferIntPtr2);
            recvData2.Append(sbResult2);
            Marshal.FreeHGlobal(bufferIntPtr);
            Marshal.FreeHGlobal(bufferIntPtr2);
            return state;
        }

        /// <summary>
        /// 获取网页数据
        /// </summary>
        /// <param name="url">地址</param>
        /// <returns>页面源码</returns>
        public static String get(String url)
        {
            String content = "";
            HttpWebRequest request = null;
            HttpWebResponse response = null;
            StreamReader streamReader = null;
            Stream resStream = null;
            try
            {
                request = (HttpWebRequest)WebRequest.Create(url);
                request.KeepAlive = false;
                request.Timeout = 10000;
                ServicePointManager.DefaultConnectionLimit = 50;
                response = (HttpWebResponse)request.GetResponse();
                resStream = response.GetResponseStream();
                streamReader = new StreamReader(resStream, Encoding.Default);
                content = streamReader.ReadToEnd();
            }
            catch (Exception ex)
            {
            }
            finally
            {
                if (response != null)
                {
                    response.Close();
                }
                if (resStream != null)
                {
                    resStream.Close();
                }
                if (streamReader != null)
                {
                    streamReader.Close();
                }
            }
            return content;
        }

        /// <summary>
        /// 数据转换为字符串
        /// </summary>
        /// <param name="datas">数据</param>
        /// <returns>字符串</returns>
        public static String securityDatasToStr(List<SecurityData> datas)
        {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < datas.Count; i++)
            {
                SecurityData data = datas[i];
                sb.AppendLine(data.m_date.ToString() + "," + data.m_close.ToString() + "," + data.m_high.ToString() + "," + data.m_low.ToString() + "," + data.m_open.ToString() + "," + data.m_volume.ToString());
            }
            return sb.ToString();
        }

        /// <summary>
        /// 计算指标
        /// </summary>
        /// <param name="formula">公式</param>
        /// <param name="datas">数据</param>
        /// <returns>结果</returns>
        public static String calculateFormula(String formula, List<SecurityData> datas, ref String shapes)
        {
            StringBuilder sb = new StringBuilder();
            StringBuilder sb2 = new StringBuilder();
            String sendStr = securityDatasToStr(datas);
            calcFormulaWithShapes(formula, sendStr, sb, sb2);
            shapes = sb2.ToString();
            return sb.ToString();
        }

        static void Main(string[] args)
        {
            String formula = "DIF:EMA(CLOSE,12)-EMA(CLOSE,26);DEA:EMA(DIF,9);MACD:(DIF-DEA)*2,COLORSTICK;";
            String httpData = get("http://quotes.money.163.com/service/chddata.html?code=0000001");
            String[] strs = httpData.Split(new String[] { "\r\n" }, StringSplitOptions.RemoveEmptyEntries);
            List<SecurityData> datas = new List<SecurityData>();
            int pos = 0;
            for (int i = 1; i < strs.Length; i++)
            {
                String str = strs[i];
                String []subStrs = str.Split(',');
                if (subStrs.Length >= 8)
                {
                    SecurityData data = new SecurityData();
                    data.m_date = i;
                    data.m_close = Convert.ToDouble(subStrs[3]);
                    data.m_high = Convert.ToDouble(subStrs[4]);
                    data.m_low = Convert.ToDouble(subStrs[5]);
                    data.m_open = Convert.ToDouble(subStrs[6]);
                    data.m_volume = Convert.ToDouble(subStrs[11]);
                    datas.Add(data);
                    pos++;
                }
            }
            //调用计算函数
            String shapes = "";
            Console.WriteLine(calculateFormula(formula, datas, ref shapes));
            Console.WriteLine(shapes);
            Console.ReadLine();
        }
    }

    /// <summary>
    /// 数据结构
    /// </summary>
    public class SecurityData
    {
        /// <summary>
        /// 日期
        /// </summary>
        public double m_date; 
        /// <summary>
        /// 收盘价
        /// </summary>
        public double m_close;
        /// <summary>
        /// 最高价
        /// </summary>
        public double m_high;
        /// <summary>
        /// 最低价
        /// </summary>
        public double m_low;
        /// <summary>
        /// 开盘价
        /// </summary>
        public double m_open;
        /// <summary>
        /// 成交量
        /// </summary>
        public double m_volume;
    }
}
