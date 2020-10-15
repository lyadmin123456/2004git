<template>
  <div class="user-order">
    <Header/>
    <div class="main">
      <div class="banner"></div>
      <div class="profile">
        <div class="profile-info">
          <div class="avatar"><img class="newImg" width="100" alt="" src="../../static/image/logo.png"></div>
          <span class="user-name">Mixtea</span>
          <span class="user-job">北京市 | Python</span>
        </div>
        <ul class="my-item">
          <li>我的账户</li>
          <li class="active">我的订单</li>
          <li>个人资料</li>
          <li>账号安全</li>
        </ul>
      </div>
      <div class="user-data">
        <ul class="nav">
          <li class="order-info">订单</li>
          <li class="course-expire">有效期</li>
          <li class="course-price">课程价格</li>
          <li class="real-price">实付金额</li>
          <li class="order-status">交易状态</li>
          <li class="order-do">交易操作</li>
        </ul>
        <div class="my-order-item" v-for="(value,index) in list" :key="index">
          <div class="user-data-header">
            <span class="order-time">{{ value.pay_time }}</span>
            <span class="order-num">订单号：
                        <span class="my-older-number">{{ value.order_number }}</span>
                    </span>
          </div>
          <ul class="nav user-data-list" v-for="(item,index) in value.order_datail_list" :key="index">
            <li class="order-info">
              <div class="order-info-title">
                <p class="course-title">{{ item.discount_name}}</p>
                <p class="price-service"></p>
              </div>
            </li>
            <li class="course-expire">永久有效</li>
            <li class="course-price">{{ item.price }}</li>
            <li class="real-price">{{ item.real_price }}</li>
            <li class="order-status">{{ item.expire }}</li>
            <li class="order-do">
              <span class="btn btn2"><router-link :to="'/detail/'+item.course_id">去学习</router-link></span>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
import Header from "./common/Header";
import Footer from "./common/Footer";
export default {
  name: "OrderList",
  components: {
    "Header": Header,
    "Footer": Footer,
  },
  data() {
    return {
      list: [],
    }
  },
  created() {
    this.order_list();
  },
  methods: {
    is_login() {
      this.token = localStorage.token || sessionStorage.token;
      if (this.token) {
        return false;
      } else {
        this.$message("请先登陆后订购");
        this.$router.push('/')
      }
    },
    order_list() {
      this.is_login()
      this.$axios({
        url:"http://127.0.0.1:8000/order/list/",
        method: "get"
      }).then(res => {
        console.log(res.data);
        this.list = res.data
      }).catch(error => {
        console.log(error)
      })
    },
  }
}
</script>

<style scoped>
.main .banner {
  width: 100%;
  height: 324px;
  background: url(../../static/image/python.jpg) no-repeat;
  background-size: cover;
  z-index: 1;
}
.profile {
  width: 1200px;
  margin: 0 auto;
}
.profile-info {
  text-align: center;
  margin-top: -80px;
}
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 60px;
  overflow: hidden;
  margin: 0 auto;
}
.user-name {
  display: block;
  font-size: 24px;
  color: #4a4a4a;
  margin-top: 14px;
}
.user-job {
  display: block;
  font-size: 11px;
  color: #9b9b9b;
}
.my-item {
  list-style: none;
  line-height: 1.42857143;
  color: #333;
  width: 474px;
  height: 31px;
  display: -ms-flexbox;
  display: flex;
  cursor: pointer;
  margin: 41px auto 0;
  -ms-flex-pack: justify;
  justify-content: space-between;
}
.my-item .active {
  border-bottom: 1px solid #000;
}
.user-data {
  width: 1200px;
  height: auto;
  margin: 0 auto;
  padding-top: 30px;
  border-top: 1px solid #e8e8e8;
  margin-bottom: 63px;
}
.nav {
  width: 100%;
  height: 60px;
  background: #e9e9e9;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}
.nav li {
  margin-left: 20px;
  margin-right: 28px;
  height: 60px;
  line-height: 60px;
  list-style: none;
  font-size: 13px;
  color: #333;
  border-bottom: 1px solid #e9e9e9;
  width: 160px;
}
.nav .order-info {
  width: 325px;
}
.nav .course-expire {
  width: 60px;
}
.nav .course-price {
  width: 130px;
}
.user-data-header {
  display: flex;
  height: 44px;
  color: #4a4a4a;
  font-size: 14px;
  background: #f3f3f3;
  -ms-flex-align: center;
  align-items: center;
}
.order-time {
  font-size: 12px;
  display: inline-block;
  margin-left: 20px;
}
.order-num {
  font-size: 12px;
  display: inline-block;
  margin-left: 29px;
}
.user-data-list {
  height: 100%;
  display: flex;
}
.user-data-list {
  background: none;
}
.user-data-list li {
  height: 60px;
  line-height: 60px;
}
.user-data-list .order-info {
  display: flex;
  align-items: center;
  margin-right: 28px;
}
.user-data-list .order-info img {
  max-width: 100px;
  max-height: 75px;
  margin-right: 22px;
}
.course-title {
  width: 203px;
  font-size: 13px;
  color: #333;
  line-height: 20px;
  margin-top: -10px;
}
.order-info-title .price-service {
  line-height: 18px;
}
.price-service {
  font-size: 12px;
  color: #fa6240;
  padding: 0 5px;
  border: 1px solid #fa6240;
  border-radius: 4px;
  margin-top: 4px;
  position: absolute;
}
.order-info-title {
  margin-top: -10px;
}
.user-data-list .course-expire {
  font-size: 12px;
  color: #ff5502;
  width: 60px;
  text-align: center;
}
.btn {
  width: 100px;
  height: 32px;
  font-size: 14px;
  color: #fff;
  background: #ffc210;
  border-radius: 4px;
  border: none;
  outline: none;
  transition: all .25s ease;
  display: inline-block;
  line-height: 32px;
  text-align: center;
  cursor: pointer;
}
</style>
