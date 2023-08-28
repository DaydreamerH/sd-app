<template>
	<view class='Card'>
		<view>
			<uv-image width="345rpx" height="345rpx"
			 :src='img_url'
			 radius="20rpx"></uv-image>
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
		height: 430rpx;
		border-radius: 20rpx;
		margin-top: 10rpx;
		margin-bottom: 10rpx;
		margin-left: 20rpx;
		margin-right: 10rpx;
		background-color: #00A8E8;
		display: block;
		.tBox {
			color: #FFF200;
			font-weight: bold;
			padding-left: 10rpx;
			padding-right: 10rpx;
		}
	}
</style>