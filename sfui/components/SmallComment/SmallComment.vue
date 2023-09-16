<template>
	<view class="SmallComment">
		<view class='info'>
			<uv-avatar class='avatar' :src='comment.avatar' size="25"></uv-avatar>
			<view class='name_time'>
				<view class='name'>{{comment.uname}}</view>
				<view class='time'>{{comment.time}}</view>
			</view>
		</view>
		<view class='main'>
			<text class='text-wrap'>
				{{comment.text}}
			</text>
		</view>	
	</view>
</template>

<script>
	export default {
		name:"SmallComment",
		props:['comment'],
		data() {
			return {
				
			};
		}
	}
</script>

<style lang="scss">
	.SmallComment{
		width: 600rpx;
		margin-left: 75rpx;
		height: auto;
		.info {
			width: auto;
			height:auto;
			display: flex;
			
			.avatar {
				margin-left: 10rpx;
				margin-right: 10rpx;
				margin-top: 15rpx;
			}
			.name_time{
				min-width: 300rpx;
				width: auto;
				margin-left: 10rpx;
				height: auto;
				display: block;
				.name {
					margin-top: 5rpx;
					font-size: 25rpx;
					width: auto;
				}
				.time {
					margin-top: 2rpx;
					font-size: 10rpx;
				}
			}
		}
		.main{
			width: auto;
			margin-left: 90rpx;
			height: auto;
			min-height: 50rpx;
			font-size:28rpx;
			.text-wrap {
				word-break: break-all;
			}
		}
	}
</style>