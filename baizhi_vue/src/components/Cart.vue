<template>
  <div class="cart">
    <Header></Header>
    <div class="cart_info">
      <div class="cart_title">
        <span class="text">我的购物车</span>
        <span class="total">{{ cart_list.length }}</span>
      </div>
      <div class="cart_table">
        <div class="cart_head_row">
          <span class="doing_row"></span>
          <span class="course_row">课程</span>
          <span class="expire_row">有效期</span>
          <span class="price_row">单价</span>
          <span class="do_more">操作</span>
        </div>
        <div class="cart_course_list">
          <CartItem v-for="(course,index) in cart_list" :key="index" :course="course"
                    @delcart="del_cart(index)" @change_select="cart_price">

          </CartItem>
        </div>
        <div class="cart_footer_row">
                    <span class="cart_select">
                        <label> <el-checkbox v-model="all_select"
                        >&nbsp;&nbsp;</el-checkbox><span @click="change_all_select">全选</span></label>
                    </span>
          <span class="cart_delete"><i class="el-icon-delete"></i> <span>删除</span></span>
          <router-link class="goto_pay" to="/order">去结算</router-link>
          <span class="cart_total">总计：¥{{total_price}}</span>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import CartItem from "./common/CartItem";
import Header from "./common/Header";
import Footer from "./common/Footer";
export default {
  name: "Cart",
  data() {
    return {
      cart_list: [],
      //购物车全部勾选的商品总价格
      total_price: 0.00,
      key: "",
      all_select: "",
    }
  },
  components: {
    CartItem, Header, Footer
  },
  // watch:{
  //     "change_all_select":function () {
  //         this.change_select()
  //     }
  // },
  created() {
    this.get_cart()
  },
  methods: {
    //检查用户是否登录
    check_user() {
      let token = localStorage.user_token || sessionStorage.user_token
      if (!token) {
        let self = this;
        this.$confirm("您尚未登录，请登录！", {
          callback() {
            self.$router.push("/login")
          }
        });
        return false
      }
      return token
    },
    //获取购物车
    get_cart() {
      let token = this.check_user();
      this.$axios.get('http://127.0.0.1:8000/cart/options/', {
        headers: {
          "Authorization": "jwt " + token,
        }
      }).then(res => {
        console.log(res.data);
        this.cart_list = res.data
        this.$store.commit("add_cart", this.cart_list.length)
        //成功后计算购物车中所有选中商品的价格
        this.cart_price()
      }).catch(error => {
        console.log(error.response);
      })
    },
    //计算购物车的商品总价
    cart_price() {
      let total = 0
      let count = 0
      let count_length = this.cart_list.length
      this.cart_list.forEach((course, key) => {
        //判断商品是否选中
        if (course.selected) {
          total = total + parseFloat(course.real_price);
          count++
        }
        this.total_price = total
        // console.log(this.total_price);
      })
      if (count === count_length) {
        this.all_select = true
      } else {
        this.all_select = false
      }
    },
    //删除后重新更新课程数量
    del_cart(key) {
      // key = 1
      this.cart_list.splice(key, 1)
      console.log(key, 111)
      this.$store.commit("add_cart", this.cart_list.length)
      this.cart_price()
    },
    // 全选反选
    change_all_select() {
      if (this.all_select) {
        let token = localStorage.user_token || sessionStorage.user_token;
        this.$axios.get('http://127.0.0.1:8000/cart/options/', {
          headers: {
            "Authorization": "jwt " + token,
          }
        }).then(response => {
          console.log(response.data);
          // this.$message.success(response.data.message)
          // this.$emit("change_select")
          this.cart_list = response.data
          this.cart_list.forEach((course, key) => {
            course.selected = 0
          })
          //成功后向状态机提交重新改变购物车长度
          this.$store.commit("add_cart", this.cart_list.length)
          this.cart_price()
        }).catch(error => {
          console.log(error.response);
          this.$message.error(error.response)
        })
      }else{
        let token = localStorage.user_token || sessionStorage.user_token;
        this.$axios.get(`${this.$settings.HOST}cart/options/`, {
          headers: {
            "Authorization": "jwt " + token,
          }
        }).then(response=>{
          console.log(response.data);
          // this.$message.success(response.data.message)
          // this.$emit("change_select")
          console.log(response.data);
          this.cart_list = response.data
          this.cart_list.forEach((course,key)=>{
            course.selected = true
          })
          //成功后向状态机提交重新改变购物车长度
          this.$store.commit("add_cart",this.cart_list.length)
          this.cart_price()
        }).catch(error=>{
          console.log(error.response);
          this.$message.error(error.response)
        })
      }
    }
  }
}
</script>

<style scoped>
.cart_info {
  width: 1200px;
  margin: 0 auto 200px;
}
.cart_title {
  margin: 25px 0;
}
.cart_title .text {
  font-size: 18px;
  color: #666;
}
.cart_title .total {
  font-size: 12px;
  color: #d0d0d0;
}
.cart_table {
  width: 1170px;
}
.cart_table .cart_head_row {
  background: #F7F7F7;
  width: 100%;
  height: 80px;
  line-height: 80px;
  padding-right: 30px;
}
.cart_table .cart_head_row::after {
  content: "";
  display: block;
  clear: both;
}
.cart_table .cart_head_row .doing_row,
.cart_table .cart_head_row .course_row,
.cart_table .cart_head_row .expire_row,
.cart_table .cart_head_row .price_row,
.cart_table .cart_head_row .do_more {
  padding-left: 10px;
  height: 80px;
  float: left;
}
.cart_table .cart_head_row .doing_row {
  width: 78px;
}
.cart_table .cart_head_row .course_row {
  width: 530px;
}
.cart_table .cart_head_row .expire_row {
  width: 188px;
}
.cart_table .cart_head_row .price_row {
  width: 162px;
}
.cart_table .cart_head_row .do_more {
  width: 162px;
}
.cart_footer_row {
  padding-left: 30px;
  background: #F7F7F7;
  width: 100%;
  height: 80px;
  line-height: 80px;
}
.cart_footer_row .cart_select span {
  margin-left: -7px;
  font-size: 18px;
  color: #666;
}
.cart_footer_row .cart_delete {
  margin-left: 58px;
}
.cart_delete .el-icon-delete {
  font-size: 18px;
}
.cart_delete span {
  margin-left: 15px;
  cursor: pointer;
  font-size: 18px;
  color: #666;
}
.cart_total {
  float: right;
  margin-right: 62px;
  font-size: 18px;
  color: #666;
}
.goto_pay {
  float: right;
  width: 159px;
  height: 80px;
  outline: none;
  border: none;
  background: #ffc210;
  font-size: 18px;
  color: #fff;
  text-align: center;
  cursor: pointer;
}
</style>
