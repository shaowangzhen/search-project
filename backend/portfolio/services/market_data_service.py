"""
市场数据服务 - 获取实时股票价格
支持多个数据源：新浪财经、腾讯财经等
"""
import asyncio
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime
import json


class MarketDataService:
    """市场数据服务"""

    def __init__(self):
        self.session = None

    async def _get_session(self):
        """获取或创建aiohttp会话"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        """关闭会话"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def get_realtime_price(self, symbol: str) -> Optional[Dict]:
        """
        获取实时价格

        Args:
            symbol: 股票代码，如 '600000.SH' 或 '000001.SZ'

        Returns:
            包含价格信息的字典，如果失败返回None
        """
        try:
            # 转换代码格式：600000.SH -> sh600000
            market_code = self._convert_symbol(symbol)

            # 使用新浪财经接口
            url = f"https://hq.sinajs.cn/list={market_code}"

            session = await self._get_session()
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    text = await response.text()
                    return self._parse_sina_response(symbol, text)
                else:
                    print(f"获取 {symbol} 价格失败，状态码: {response.status}")
                    return None

        except Exception as e:
            print(f"获取 {symbol} 价格出错: {e}")
            return None

    async def get_realtime_prices(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        批量获取实时价格

        Args:
            symbols: 股票代码列表

        Returns:
            字典，键为股票代码，值为价格信息
        """
        tasks = [self.get_realtime_price(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)

        # 构建结果字典
        price_data = {}
        for symbol, result in zip(symbols, results):
            if result:
                price_data[symbol] = result

        return price_data

    def _convert_symbol(self, symbol: str) -> str:
        """
        转换股票代码格式
        600000.SH -> sh600000
        000001.SZ -> sz000001
        """
        if '.' in symbol:
            code, market = symbol.split('.')
            market = market.lower()
            return f"{market}{code}"
        return symbol

    def _parse_sina_response(self, symbol: str, response_text: str) -> Optional[Dict]:
        """
        解析新浪财经接口返回的数据

        格式: var hq_str_sh600000="浦发银行,8.55,8.54,8.52,..."
        """
        try:
            # 提取引号中的数据
            start_idx = response_text.find('"')
            end_idx = response_text.rfind('"')
            if start_idx == -1 or end_idx == -1:
                return None

            data = response_text[start_idx + 1:end_idx].split(',')

            if len(data) < 32:  # 新浪接口返回至少32个字段
                return None

            return {
                'symbol': symbol,
                'name': data[0],  # 股票名称
                'current_price': float(data[3]),  # 当前价格
                'prev_close': float(data[2]),  # 昨收价
                'open': float(data[1]),  # 今开价
                'high': float(data[4]),  # 最高价
                'low': float(data[5]),  # 最低价
                'volume': float(data[8]),  # 成交量（手）
                'amount': float(data[9]),  # 成交额（元）
                'change': float(data[3]) - float(data[2]),  # 涨跌额
                'change_percent': (float(data[3]) - float(data[2])) / float(data[2]) * 100 if float(data[2]) > 0 else 0,  # 涨跌幅
                'timestamp': datetime.now().isoformat(),
                'date': data[30],  # 日期
                'time': data[31],  # 时间
            }

        except Exception as e:
            print(f"解析新浪数据失败: {e}")
            return None

    async def get_historical_prices(self, symbol: str, days: int = 30) -> Optional[List[Dict]]:
        """
        获取历史价格数据

        Args:
            symbol: 股票代码
            days: 获取最近N天的数据

        Returns:
            历史价格列表
        """
        # 这里可以接入更多的数据源，如东方财富、tushare等
        # 简化实现，返回空列表
        print(f"获取 {symbol} 最近 {days} 天的历史数据（待实现）")
        return []

    async def search_stock(self, keyword: str) -> List[Dict]:
        """
        搜索股票

        Args:
            keyword: 搜索关键词（股票代码或名称）

        Returns:
            匹配的股票列表
        """
        try:
            # 使用腾讯财经搜索接口
            url = f"https://smartbox.gtimg.cn/s3/?q={keyword}&t=gp"

            session = await self._get_session()
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    text = await response.text()
                    return self._parse_search_response(text)

        except Exception as e:
            print(f"搜索股票出错: {e}")

        return []

    def _parse_search_response(self, response_text: str) -> List[Dict]:
        """解析股票搜索结果"""
        try:
            # 腾讯接口返回格式: v_hint="sh600000~浦发银行~..."
            results = []

            if 'v_hint=' in response_text:
                start_idx = response_text.find('"')
                end_idx = response_text.rfind('"')
                if start_idx != -1 and end_idx != -1:
                    data = response_text[start_idx + 1:end_idx]

                    # 分割多个结果
                    items = data.split('^')
                    for item in items:
                        if not item:
                            continue
                        parts = item.split('~')
                        if len(parts) >= 3:
                            # 转换格式: sh600000 -> 600000.SH
                            code = parts[0]
                            market = code[:2].upper()
                            symbol_code = code[2:]

                            results.append({
                                'symbol': f"{symbol_code}.{market}",
                                'name': parts[1],
                                'type': parts[2] if len(parts) > 2 else 'stock'
                            })

            return results

        except Exception as e:
            print(f"解析搜索结果失败: {e}")
            return []


# 创建全局实例
market_data_service = MarketDataService()
