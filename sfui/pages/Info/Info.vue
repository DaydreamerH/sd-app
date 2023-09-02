<template>
	<view class="row">
		<view class="InfoCard">
			<view class="LoginText">修改信息</view>
			<uv-form v-model="u_info">
				<view style="display: flex;">
					<uv-avatar :src="u_info.avatar" shape="square" size="70" class='Avatar'></uv-avatar>
					<uv-upload :maxCount="1" :previewFullImage="true" @afterRead="afterRead"></uv-upload>
				</view>
				<uv-form-item label="昵称" class="input-item">
					<uv-input class="inputbox" placeholder="请输入昵称" v-model="u_info.uname"></uv-input>
				</uv-form-item>
				<uv-form-item label="签名" class="input-item">
					<uv-input class="inputbox" placeholder="请输入签名" v-model="u_info.sign"></uv-input>
				</uv-form-item>
			</uv-form>
			<uv-button class="button" @click="UpInfo" type="primary" plain>修改信息</uv-button>
			<uv-button class="button" @click="LogOut" type="primary">退出登录</uv-button>
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
				},
			}
		},
		methods: {
			UpInfo() {
				let _this = this
				uni.request({
					url: "http://localhost:3689/user/upInfo",
					data: _this.u_info,
					method: 'POST'
				}).then(function(resp) {
					if (resp.data == 'success') {
						uni.showToast({
							title: "修改成功"
						})
						uni.reLaunch({
							url: '/pages/MySpace/MySpace'
						})
					} else {
						uni.showToast({
							title: "修改失败",
							icon: 'error'
						})
					}
				}).catch(e => {
					console.log(e)
					uni.showToast({
						title: "修改失败",
						icon: 'error'
					})
				})
			},
			async afterRead(event) {
				let file = event.file
				let _this = this
				uni.uploadFile({
					url: "http://localhost:3689/user/upAvatar",
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
				uni.removeStorage({
					key: "u_info"
				})
				uni.reLaunch({
					url: "/pages/MySpace/MySpace"
				})
			}
		},
		onLoad(option){
			this.u_info.uname = option.uname
			this.u_info.avatar = option.avatar
			this.u_info.sign = option.sign
			let _this = this
			uni.getStorage({
				key:'u_info',
				success(res){
					_this.u_info.uid = res.data.uid
					_this.u_info.secret = res.data.secret
				}
			})
		}
	}
</script>

<style lang="scss" scoped>
	.LoginText {
		width: 200rpx;
		height: auto;
		position: relative;
		top: 40rpx;
		left: 250rpx;
		background-color: white;
		text-align: center;
		font-size: 50rpx;
		font-weight: bold;
		margin-bottom: 60rpx;
	}

	.row {
		width: 750rpx;
		height: 100vh;
		background-color: black;

		.InfoCard {
			width: 700rpx;
			height: auto;
			background-color: white;
			border-radius: 30rpx;
			padding: 5rpx;
			margin-bottom: 10rpx;
			position: absolute;
			left: 25rpx;
			top: 50rpx;

			.input-item {
				padding-left: 15rpx;
				margin-bottom: 10rpx;

				.inputbox {
					margin-right: 15rpx;
				}
			}
		}
	}

	.button {
		width: 200rpx;
		margin-left: 250rpx;
		margin-bottom: 50rpx;
	}
	
	.Avatar{
		margin-left: 10rpx;
		margin-right: 20rpx;
	}
	
</style>