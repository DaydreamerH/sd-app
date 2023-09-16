<template>
	<view class='CommentInfoBox'>
		<uv-avatar class='avatar' :src='info.avatar'></uv-avatar>
		<view class='MainBox'>
			<view class='unameBox'>{{info.uname}}</view>
			<view class='unameBOx'>在&ensp;{{info.title}}&ensp;回复了你:</view>
			<view class='NewComment'>{{info.text}}</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: "CommentInfo",
		props:['info'],
		data() {
			return {

			};
		}
	}
</script>

<style lang="scss" scoped>
	.CommentInfoBox {
		width: 750rpx;
		height: auto;
		min-height: 200rpx;
		display: flex;
		padding-top: 20rpx;
		padding-left: 20rpx;
		padding-right: 20rpx;
		.avatar {
			margin-top: 10rpx;
			margin-right: 40rpx;
		}

		.MainBox {
			width: auto;
			.unameBox {
				min-width: 100rpx;
				min-height: 50rpx;
			}
			.NewComment{
				margin-top: 10rpx;
				font-size: 40rpx;
			}
		}
	}
</style>