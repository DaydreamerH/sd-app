<template>
	<view class="row">
		<uv-toast ref='toast'></uv-toast>
		<view class="LoginCard">
			<view class="LoginText">登录</view>
			<uv-form v-model="form">
				<uv-form-item label="账户" class="input-item">
					<uv-input class="inputbox" placeholder="请输入账户" v-model="form.uid"></uv-input>
				</uv-form-item>
				<uv-form-item label="密码" class="input-item">
					<uv-input class="inputbox" placeholder="请输入密码" type="password" v-model="form.secret"></uv-input>
				</uv-form-item>
			</uv-form>
			<uv-button class="button" color=" #FF5A5F" @click="login">登录</uv-button>
			<uv-button class="button" color=" #FF5A5F" @click="toRegister">注册</uv-button>
		</view>
	</view>
</template>

<script>
import { aes_encrypt } from '../../encode/util';
	export default {
		name: "login",
		data() {
			return {
				form: {
					uid: "",
					secret: ""
				},
			};
		},
		methods: {
			login(){
				if(this.form.uid=="")
					this.$refs.toast.show({
						message:'账户不得为空',
						type:'error',
						position:'top'
					})
				else if(this.form.secret=='')
					this.$refs.toast.show({
						message:'密码不得为空',
						type:'error',
						position:'top'
					})
				else if(this.form.uid.length>20||this.form.secret.length>20){
					this.$refs.toast.show({
						message:'账户或密码错误',
						type:'error',
						position:'top'
					})
				}
				else {
					let _this = this
					this.form.secret = aes_encrypt(this.form.secret)
					uni.request({
						url:"http://localhost:3689/user/login",
						method:"POST",
						data:_this.form
					}).then(function(resp){
						if(resp.data=="success"){
							_this.$refs.toast.show({
								message:'登录成功',
								type:'success',
								position:'top',
								complete:function(){
									uni.setStorageSync('u_info',{
										uid:_this.form.uid,
										secret:_this.form.secret
									})
									uni.reLaunch({
										url:"/pages/MySpace/MySpace"
									})
								}	
							})
						}
						else{
							_this.$refs.toast.show({
								message:'账户或密码错误',
								type:'error',
								position:'top'
							})
							_this.form.secret=''
						}
					}).catch(e=>{
						console.log(e)
						_this.$refs.toast.show({
							message:'服务器出现错误，稍后尝试',
							type:'error',
							position:'top'
						})
						_this.form.secret=''
					})
				}
			},
			toRegister(){
				uni.navigateTo({
					url:"/pages/Register/Register"
				})
			}
		},
		mounted(){
			
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;
		background-image: url("../../static/loginBackground/loginback.jpg");
		background-size: 750rpx 100vh;
	}

	.LoginText {
		width: 200rpx;
		height: auto;
		position: relative;
		top: 40rpx;
		left: 225rpx;
		background-color: white;
		text-align: center;
		font-size: 50rpx;
		font-weight: bold;
		margin-bottom: 60rpx;
	}

	.LoginCard {
		background-color: white;
		height: auto;
		width: 650rpx;
		position: absolute;
		left: 50rpx;
		top: 250rpx;
		opacity: 0.97;
		border-top: 1px solid #ffffff;
		box-shadow: grey 10px 10px 30px 5px  ;//边框阴影
		border-radius: 30rpx;
		padding: 10rpx;
		
	}

	.input-item {
		padding-left: 15rpx;
		margin-bottom: 30rpx;
		.inputbox {
			margin-right: 15rpx;
		}
	}


	.button {
		width: 200rpx;
		margin-left: 225rpx;
		margin-bottom: 50rpx;
	}
</style>
