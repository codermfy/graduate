import Xlsx from "xlsx";
export function debounce(func,wait,immediate) {
  let timeout;

  return function () {
      let context = this;
      let args = arguments;

      if (timeout) clearTimeout(timeout);
      if (immediate) {
          var callNow = !timeout;
          timeout = setTimeout(() => {
              timeout = null;
          }, wait)
          if (callNow) func.apply(context, args)
      }
      else {
          timeout = setTimeout(function(){
              func.apply(context, args)
          }, wait);
      }
  }
}
//时间格式化，传入date和’YYYY-MM-dd hh-mm-ss'
export function formatDate(date, fmt) {
  //获取年份
  if (/(Y+)/.test(fmt)) {
    let dateY = date.getFullYear() + "";
    //RegExp.$1 在判断中出现过，且是括号括起来的，所以 RegExp.$1 就是 "yyyy"
    fmt = fmt.replace(RegExp.$1, dateY.substr(4 - RegExp.$1.length));
  }

  //获取其他
  let o = {
    "M+": date.getMonth() + 1,
    "d+": date.getDate(),
    "h+": date.getHours(),
    "m+": date.getMinutes(),
    "s+": date.getSeconds()
  };
  for (const k in o) {
    if (new RegExp(`(${k})`).test(fmt)) {
      let str = o[k] + "";
      fmt = fmt.replace(
        RegExp.$1,
        RegExp.$1.length == 1 ? str : padLeftZero(str)
      );
    }
  }
  return fmt;
}
function padLeftZero(str) {
  return ("00" + str).substr(str.length);
}
export function file2Xce(file) {
  return new Promise(function (resolve, reject) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const data = e.target.result;
      this.wb = Xlsx.read(data, {
        type: "binary",
      });
      const result = [];
      this.wb.SheetNames.forEach((sheetName) => {
        result.push({
          sheetName: sheetName,
          sheet: Xlsx.utils.sheet_to_json(this.wb.Sheets[sheetName]),
        });
      });
      resolve(result);
    };
    reader.readAsBinaryString(file.raw);
  });
}