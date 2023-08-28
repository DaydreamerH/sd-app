<template>
	<view class='Card'>
		<view>
			<uv-image width="345rpx" height="345rpx"
			 :src='img_url' class='image'></uv-image>
			<text class='tBox'>{{title}}</text>
		</view>
	</view>
</template>

<script>
	export default {
		name: "ImgCard",
		props:['img_url','title'],
		data() {
			return {

			};
		}
	}
</script>

<style lang="scss" scoped>
	.Card {
		width: 345rpx;
		min-height: 420rpx;
		height: auto;
		border-radius: 10rpx;
		margin-top: 10rpx;
		margin-bottom: 10rpx;
		margin-left: 20rpx;
		margin-right: 10rpx;
		display: block;
		background-color:#D2E8E8;
		border: #2A9D8F 3rpx solid;
		box-shadow:0 15px 35px rgba(0,0,0,0.1);
		.image{
			margin-bottom: 5rpx;
		}
		.tBox {
			padding-left: 10rpx;
			padding-right: 10rpx;
			color:#2A9D8F;
			font-size: 30rpx;
		}
	}
</style>