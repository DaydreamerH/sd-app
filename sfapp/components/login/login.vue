<template>
	<view class="row">
		<view class="LoginCard">
			<view class="LoginText">登录</view>
			<form>
				<view class="LoginInput">
					<text class="tip">账号</text>
					<u-input border="border" name="uid"/>
				</view>
				<view class="LoginInput">
					<text class="tip">密码</text>
				</view>
			</form>
		</view>
	</view>
</template>

<script>
	export default {
		name: "login",
		data() {
			return {

			};
		},
		methods: {
			submit() {

			}
		}
	}
</script>

<style lang="scss">
	.row {
		width: 750rpx;
		height: 100vh;
		background-color: #f3f4f6;
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
	}

	.LoginInput {
		width: 600rpx;
		position: relative;
		height: auto;
		left: 3rpx;
		
		background-color: white;
		margin-bottom: 70rpx;

		.tip {
			position: relative;
			left: 20rpx;
			top: 22rpx;
			font-size: large;
			text-align: center;
		}
		.inputbox {
			width: 500rpx;
			position: relative;
			left: 110rpx;
			height: 100%;
			border-radius: 10rpx;
			border: 1px brown;

		}
	}
</style>