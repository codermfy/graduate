//  在根目录添加一个  vue.config.js  文件
//   重启项目
module.exports = {
    //以下配置的效果
    //   “/api/getok.php”  -->   
  // 修改的配置
  devServer: {
      proxy: {
          //如果地址以/api开头，它就会请求到 
          '/api': {
              target: 'http://172.29.0.155:5000',
              changeOrigin: true,
              ws: true, 
              pathRewrite: {
   				 '^/api': '',   //重写请求路径
 			 },
          },
          '/file': {
            target: 'http://192.168.3.31:8000',
            changeOrigin: true,
            ws: true, 
            pathRewrite: {
                '^/file': '',   //重写请求路径
            },
        }
      }
  }
}