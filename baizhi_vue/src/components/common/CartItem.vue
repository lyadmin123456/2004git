<template>
  <div class="cart_item">
    <div class="cart_column column_1">
      <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
    </div>
    <div class="cart_column column_2">
      <img :src="course.course_img" alt="">
      <span><router-link :to="'/course/detail/'+course.id">{{course.name}}</router-link></span>
    </div>
    <div class="cart_column column_3">
      <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
        <el-option :label="item.expire_text" :value="item.id" :key="item.id" v-for="item in course.expire_list"></el-option>
      </el-select>
    </div>
    <div class="cart_column column_4">¥{{course.real_price.toFixed(2)}}</div>
    <div class="cart_column column_4" @click="delcart(course.id)"><button>删除</button></div>
  </div>
</template>

<script>
export default {
  name: "CartItem",
  //接受父组件传递来的课程参数
  props: ["course"],
  watch: {
    "course.selected": function () {
      //后台发送请求切换状态
      this.change_select()
    },
    //课程有效期切换
    "course.expire_id":function () {
      this.change_expire()
    }
  },
  methods: {
    //状态切换方法
    change_select() {
      let token = localStorage.user_token || sessionStorage.user_token;
      this.$axios.patch('http://127.0.0.1:8000/cart/options/', {
        selected: this.course.selected,
        course_id: this.course.id
      }, {
        headers: {
          "Authorization": "jwt " + token,
        }
      }).then(response=>{
        console.log(response.data);
        this.$message.success(response.data.message)
        this.$emit("change_select")
      }).catch(error=>{
        console.log(error.response);
        this.$message.error(error.response)
      })
    },
    //有效期切换方法
    change_expire(){
      let token = localStorage.user_token || sessionStorage.user_token
      this.$axios.put('http://127.0.0.1:8000/cart/options/',{
        expire_id : this.course.expire_id,
        course_id : this.course.id
      },{
        headers: {
          "Authorization": "jwt " + token,
        }
      }).then(res=>{
        console.log(res.data);
        //有效期切换后，价格改变重新赋值
        this.course.real_price = res.data.real_price
        this.$message.success(res.data.message)
        this.$emit("change_select")
      }).catch(error=>{
        console.log(error);
      })
    },
    //删除购物车内容
    delcart(course_id){
      let token = localStorage.user_token || sessionStorage.user_token;
      this.$axios.delete('http://127.0.0.1:8000/cart/delcart/'+`${course_id}`,{
        headers: {
          "Authorization": "jwt " + token,}
      }).then(res=>{
        this.$message.success(res.data.message)
        // this.check_user()
        // this.get_cart()
        // location.reload()
        //删除商品时调用父组件的方法，重新执行计算总价的方法
        this.$emit("delcart")
      }).catch(error=>{
        console.log(error.response);
        this.$message.error("删除失败！")
      })
    }
  },
  data() {
    return {
      expire: "一个月有效"
    }
  }
}
</script>

<style scoped>
.cart_item::after {
  content: "";
  display: block;
  clear: both;
}
.cart_column {
  float: left;
  height: 250px;
}
.cart_item .column_1 {
  width: 88px;
  position: relative;
}
.my_el_checkbox {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  margin: auto;
  width: 16px;
  height: 16px;
}
.cart_item .column_2 {
  padding: 67px 10px;
  width: 520px;
  height: 116px;
}
.cart_item .column_2 img {
  width: 175px;
  height: 115px;
  margin-right: 35px;
  vertical-align: middle;
}
.cart_item .column_3 {
  width: 197px;
  position: relative;
  padding-left: 10px;
}
.my_el_select {
  width: 117px;
  height: 28px;
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
}
.cart_item .column_4 {
  padding: 67px 10px;
  height: 116px;
  width: 142px;
  line-height: 116px;
}
</style>
