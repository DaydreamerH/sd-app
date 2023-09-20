<template>
	<view class="row">
		<uv-toast ref="toast"></uv-toast>
		<view class="LoginCard">
			<view class="LoginText">注册</view>
			<uv-form v-model="form">
				<uv-form-item label="昵称" class="input-item">
					<uv-input class="inputbox" placeholder="请输入昵称(不超过20字)" v-model="form.uname" maxlength="20"></uv-input>
				</uv-form-item>
				<uv-form-item label="账户" class="input-item">
					<uv-input class="inputbox" placeholder="请输入账户(20位以内)" v-model="form.uid" maxlength="20"></uv-input>
				</uv-form-item>
				<uv-form-item label="密码" class="input-item">
					<uv-input class="inputbox" placeholder="请输入密码(20位以内)" type="password" v-model="form.secret" maxlength="20"></uv-input>
				</uv-form-item>
				<uv-form-item label="确认密码" class="input-item">
					<uv-input class="inputbox" placeholder="请输入密码(20位以内)" type="password" v-model="check_secret" maxlength="20"></uv-input>
				</uv-form-item>
			</uv-form>
			<uv-button class="button" color="#FF5A5F" @click="register">注册</uv-button>
			<uv-button class="button" color="#FF5A5F" plain @click="toLogin">登录</uv-button>
		</view>
	</view>
</template>

<script>
import { aes_encrypt } from '../../encode/util';
	export default {
		name: "register",
		data() {
			return {
				form: {
					uid: "",
					secret: "",
					uname: ""
				},
				check_secret: ""
			};
		},
		methods: {
			register() {
				if (this.form.secret != this.check_secret) {
					this.$refs.toast.show({
						message:'密码输入不一致',
						type:'error',
						position:"top"
					})
					this.form.secret =''
					this.check_secret =''
				} else if (this.form.uid == "" || this.form.secret == "" || this.form.uname == "") {
					this.$refs.toast.show({
						message:'存在信息未填',
						type:'error',
						position:"top"
					})
				} else if (this.form.uid.length > 20 || this.form.secret.length > 20 || this.form.uname.length > 20) {
					this.$refs.toast.show({
						message:'各项均不超过20字',
						type:'error',
						position:"top"
					})
				} else {
					let _this = this
					this.form.secret = aes_encrypt(this.form.secret)
					uni.request({
						url: "http://8.137.96.56:3689/user/register",
						method: "post",
						data: _this.form
					}).then(function(resp) {
						if (resp.data == "success") {
							this.$refs.toast.show({
								message:'注册成功',
								type:'success',
								position:"top",
								complete:function(){
									uni.setStorageSync('u_info',{
										uid:_this.form.uid,
										secret:_this.form.secret
									})
									uni.reLaunch({
										url: "/pages/MySpace/MySpace"
									})
								}
							})
						} else {
							_this.$refs.toast.show({
								message:'账户已被注册',
								type:"error",
								position:'top'
							})
							_this.form.secret=''
							_this.check_secret=''
						}
					}).catch(e => {
						console.log(e)
						_this.$refs.toast.show({
							message:'账户已被注册',
							type:"error",
							position:'top'
						})
						_this.form.secret=''
						_this.check_secret=''
					})
				}
			},
			toLogin() {
				uni.navigateTo({
					url: "/pages/Login/Login"
				})
			}
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
		top: 70rpx;
		opacity: 0.97;
		border-top: 1px solid #ffffff;
		box-shadow: grey 10px 10px 30px 5px; //边框阴影
		border-radius: 30rpx;
		padding: 10rpx;

	}

	.input-item {
		padding-left: 15rpx;
		margin-bottom: 30rpx;
	}

	.inputbox {
		margin-right: 15rpx;
	}

	.button {
		width: 200rpx;
		margin-left: 225rpx;
		margin-bottom: 50rpx;
	}
</style>