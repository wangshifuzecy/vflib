export const getCurrentTime = () => {
    const now = new Date();

    // 获取年、月、日、时、分、秒
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // 月份从 0 开始，需加 1，并补足两位
    const day = String(now.getDate()).padStart(2, '0'); // 日补足两位
    const hours = String(now.getHours()).padStart(2, '0'); // 小时补足两位
    const minutes = String(now.getMinutes()).padStart(2, '0'); // 分钟补足两位
    const seconds = String(now.getSeconds()).padStart(2, '0'); // 秒补足两位

    // 构建格式化后的日期时间字符串
    const formattedDateTimeString = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

    return formattedDateTimeString;
}
