<template>
	<view class="row">
		<uv-toast ref="toast"></uv-toast>
		<view class="InfoCard">
			<view class="LoginText">修改信息</view>
			<uv-form v-model="u_info">
				<view style="display: flex;">
					<uv-avatar :src="u_info.avatar" shape="square" size="80" class='Avatar'></uv-avatar>
					<uv-upload :maxCount="1" @afterRead="afterRead"></uv-upload>
				</view>
				<uv-form-item label="昵称" class="input-item">
					<uv-input class="inputbox" placeholder="请输入昵称" v-model="u_info.uname"></uv-input>
				</uv-form-item>
				<uv-form-item label="签名" class="input-item">
					<uv-input class="inputbox" placeholder="请输入签名" v-model="u_info.sign"></uv-input>
				</uv-form-item>
			</uv-form>
			<uv-button class="button" @click="UpInfo" color=" #FF5A5F">修改信息</uv-button>
			<uv-button class="button" @click="LogOut" color=" #FF5A5F" plain>退出登录</uv-button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				u_info: {
					uname: "",
					sign: "",
					avatar: "",
					uid: "",
					secret: ""
				}
			}
		},
		methods: {
			UpInfo() {
				if (!this.infoCheck()) return false
				let _this = this
				uni.request({
					url: "http://8.137.96.56:3689/user/upInfo",
					data: _this.u_info,
					method: 'POST'
				}).then(function(resp) {
					if (resp.data == 'success') {
						_this.$refs.toast.show({
							message: '修改成功',
							type: 'success',
							complete: function() {
								uni.reLaunch({
									url: '/pages/MySpace/MySpace'
								})
							}
						})
					} else {
						_this.$refs.toast.show({
							message: '修改失败，请检查信息是否正确',
							type: 'error'
						})
					}
				}).catch(e => {
					console.log(e)
					_this.$refs.toast.show({
						message: '服务器内部出错',
						type: 'error'
					})
				})
			},
			infoCheck() {
				if (this.u_info.uname == "") {
					this.$refs.toast.show({
						message: '昵称不得为空',
						type: 'error'
					})
					return false
				} else if (this.u_info.uname.length > 20) {
					this.$refs.toast.show({
						message: '昵称不得超过20字',
						type: 'error'
					})
					return false
				} else if (this.u_info.sign.length > 20) {
					this.$refs.toast.show({
						message: '签名不得超过20字',
						type: 'error'
					})
					return false
				}
				return true
			},
			async afterRead(event) {
				let file = event.file
				let _this = this
				uni.uploadFile({
					url: "http://8.137.96.56:3689/user/upAvatar",
					filePath: file.url,
					name: 'avatar',
					formData: {
						'uid': _this.u_info.uid,
						'secret': _this.u_info.secret
					}
				}).then(function(resp) {
					_this.u_info.avatar = resp.data
				})
			},
			LogOut() {
				uni.removeStorageSync('u_info')
				uni.reLaunch({
					url: "/pages/MySpace/MySpace"
				})
			}
		},
		onLoad(option) {
			this.u_info.uname = option.uname
			this.u_info.avatar = option.avatar
			this.u_info.sign = option.sign
			let _this = this
			this.u_info.uid = uni.getStorageSync('u_info').uid
			this.u_info.secret = uni.getStorageSync('u_info').secret
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;
		background-image: url("../../static/loginBackground/loginback.jpg");
		background-size: 750rpx 100vh;
		position: absolute;
		top: 0;

		.InfoCard {
			width: 700rpx;
			height: auto;
			border-radius: 30rpx;
			padding: 5rpx;
			margin-bottom: 10rpx;
			margin-top: 300rpx;
			margin-left: 25rpx;
			background-color: white;

			.button {
				width: 200rpx;
				margin-left: 250rpx;
				margin-bottom: 50rpx;
			}

			.Avatar {
				margin-left: 10rpx;
				margin-right: 20rpx;
			}

			.LoginText {
				width: 200rpx;
				height: auto;
				margin-left: 250rpx;
				margin-top: 40rpx;
				background-color: white;
				text-align: center;
				font-size: 50rpx;
				font-weight: bold;
				margin-bottom: 60rpx;
			}

			.input-item {
				padding-left: 15rpx;
				margin-bottom: 10rpx;

				.inputbox {
					margin-right: 15rpx;
				}
			}
		}
	}
</style>