<template>
	<view class="row">
		<view class="Infocard" @click="toInfoOrLogin">
			<view class="AvatarBox">
				<uv-avatar :src="u_info.avatar" size=70 class="Avatar" shape="square"></uv-avatar>
			</view>
			<text class="Name" v-if="u_info.uname != ''">{{u_info.uname}}</text>
			<text class="Name" v-if="u_info.uname ==''">登录</text>
			<text class="Sign" v-if="u_info.uname !=''">{{u_info.sign}}</text>
		</view>
		<uv-line></uv-line>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				u_info: {
					uid: "",
					uname: "",
					sign: "",
					avatar: "",
					secret: ""
				}
			};
		},
		methods: {
			toInfoOrLogin() {
				if (this.u_info.uid != '')
					uni.navigateTo({
						url: '/pages/Info/Info'
					})
				else uni.navigateTo({
					url: '/pages/Login/Login'
				})
			},
			test() {
				uni.navigateTo({
					url: '/pages/Login/Login'
				})
			}
		},
		mounted() {
			let _this = this
			uni.getStorage({
				key: "u_info",
				success(res) {
					_this.u_info.secret = res.data.secret
					_this.u_info.uid = res.data.uid
					uni.request({
						url: "http://localhost:3689/user/getInfo",
						data: _this.u_info,
						method: 'POST'
					}).then(function(resp) {
						_this.u_info = resp.data[0]
					})
				}
			})
		},
		onShow() {
			let _this = this
			uni.getStorage({
				key: "u_info",
				success(res) {
					_this.u_info.secret = res.data.secret
					_this.u_info.uid = res.data.uid
					uni.request({
						url: "http://localhost:3689/user/getInfo",
						data: _this.u_info,
						method: 'POST'
					}).then(function(resp) {
						_this.u_info = resp.data[0]
					})
				}
			})
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;
		background-color: white;
		background-image: url('../../static/00005-3359371929.0.png');
		background-size: 750rpx 100vh;
	}

	.Infocard {
		width: 700rpx;
		height: 260rpx;
		display: flex;
		background-color: white;
		position: absolute;
		left:20rpx;
		top:30rpx;
		border-top: 1px solid #ffffff;
		box-shadow: grey 2px 2px 2px 2px  ;//边框阴影
		border-radius: 30rpx;
		padding: 10rpx;
		opacity: 0.94;
		.AvatarBox {
			width: 200rpx;
			height: auto;
			margin: 0rpx;

			.Avatar {
				position: relative;
				left: 50rpx;
				top: 60rpx;
			}
		}

		.Name {
			position:absolute;
			left: 225rpx;
			top: 50rpx;
			font-size: 60rpx;
			font-weight: bold;
		}

		.Sign {
			position: absolute;
			top: 160rpx;
			left: 225rpx;
		}
		
	}
</style>